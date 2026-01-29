# 🚀 Guia Completo de Deploy - Ativo Real

## 📦 O Que Foi Implementado

### **Fine-Tuning Infrastructure**
✅ Application Insights com telemetria  
✅ Alertas automáticos de falha de jobs  
✅ Managed Identity para acesso seguro  
✅ Tags de custo e governança  
✅ Auto-scaling de GPUs (0-3 instâncias)  
✅ Pipeline CI/CD GitHub Actions  
✅ Validador de datasets JSONL  

### **Ativo Real Backend**
✅ Azure Cosmos DB NoSQL com queries geoespaciais  
✅ Azure Cache for Redis para performance  
✅ Containers otimizados (RuralProperties, UrbanProperties, Users, AuditLogs)  
✅ Endpoint de IA `/api/ai/chat` com chatbot  
✅ Decorators para cache e validação  
✅ Log de auditoria automático  

### **Ativo Real Frontend**
✅ Componente AIChat integrado  
✅ UI moderna com gradientes e animações  
✅ Histórico de conversação com Redis  

---

## 🛠️ Pré-requisitos

```bash
# Ferramentas necessárias
- Azure CLI (az)
- Azure Functions Core Tools
- Python 3.11
- Node.js 18+
- Git
```

---

## 📋 Deploy Passo a Passo

### **1. Configurar Azure CLI**

```bash
# Login no Azure
az login

# Definir subscription ativa
az account set --subscription "SUA_SUBSCRIPTION_ID"

# Criar Resource Group
az group create \
  --name rg-ativoreal-prod \
  --location eastus
```

### **2. Deploy Fine-Tuning Infrastructure**

```bash
cd microsoft_phi-silica-3.6_v1/lora/infra/provision

# Deploy do Bicep
az deployment group create \
  --resource-group rg-ml-finetuning \
  --template-file finetuning.bicep \
  --parameters finetuning.parameters.json

# Capturar outputs
STORAGE_ACCOUNT=$(az deployment group show \
  --resource-group rg-ml-finetuning \
  --name finetuning \
  --query 'properties.outputs.STORAGE_ACCOUNT_NAME.value' -o tsv)

echo "Storage Account: $STORAGE_ACCOUNT"
```

### **3. Deploy Ativo Real Infrastructure**

```bash
cd ativo-real/infra

# Deploy completo
az deployment group create \
  --resource-group rg-ativoreal-prod \
  --template-file main.bicep \
  --parameters main.parameters.json \
  --output json > deployment-output.json

# Extrair connection strings
COSMOS_CONN=$(jq -r '.properties.outputs.cosmosDbConnectionString.value' deployment-output.json)
REDIS_CONN=$(jq -r '.properties.outputs.redisConnectionString.value' deployment-output.json)
APP_INSIGHTS_CONN=$(jq -r '.properties.outputs.appInsightsConnectionString.value' deployment-output.json)

echo "✅ Infraestrutura criada com sucesso!"
```

### **4. Configurar GitHub Secrets (para CI/CD)**

```bash
# No repositório GitHub, vá em Settings > Secrets > Actions
# Adicione os seguintes secrets:

AZURE_CREDENTIALS: 
{
  "clientId": "<CLIENT_ID>",
  "clientSecret": "<CLIENT_SECRET>",
  "subscriptionId": "<SUBSCRIPTION_ID>",
  "tenantId": "<TENANT_ID>"
}

PHI_SILICA_ENDPOINT: "<URL_DO_MODELO_HOSPEDADO>"
PHI_SILICA_API_KEY: "<CHAVE_API>"
```

### **5. Deploy Azure Functions (Backend)**

```bash
cd ativo-real/api

# Instalar dependências
pip install -r requirements_cosmosdb.txt

# Publicar Functions
FUNCTION_APP_NAME=$(jq -r '.properties.outputs.functionAppUrl.value' ../infra/deployment-output.json | sed 's/https:\/\///' | sed 's/\..*//')

az functionapp deployment source config-zip \
  --resource-group rg-ativoreal-prod \
  --name $FUNCTION_APP_NAME \
  --src $(zip -r - . | base64)

echo "✅ Backend publicado!"
```

### **6. Deploy Static Web App (Frontend)**

```bash
cd ativo-real

# Instalar dependências
npm install

# Build
npm run build

# Deploy para Static Web App
STATIC_WEB_APP=$(jq -r '.properties.outputs.staticWebAppUrl.value' infra/deployment-output.json)

az staticwebapp upload \
  --name ativoreal-web-<suffix> \
  --resource-group rg-ativoreal-prod \
  --source dist/

echo "✅ Frontend publicado em: $STATIC_WEB_APP"
```

### **7. Configurar Variáveis de Ambiente**

```bash
# Atualizar Function App settings
az functionapp config appsettings set \
  --resource-group rg-ativoreal-prod \
  --name $FUNCTION_APP_NAME \
  --settings \
    "PHI_SILICA_ENDPOINT=<URL_DO_MODELO>" \
    "PHI_SILICA_API_KEY=<CHAVE_API>"
```

---

## 🧪 Testar Endpoints

### **Health Check**
```bash
curl https://$FUNCTION_APP_NAME.azurewebsites.net/api/health
```

### **Cadastro Rural**
```bash
curl -X POST https://$FUNCTION_APP_NAME.azurewebsites.net/api/rural/onboard \
  -H "Content-Type: application/json" \
  -d '{
    "farmName": "Fazenda Teste",
    "document": "12345678",
    "area": 500,
    "adminName": "João Silva",
    "adminCpf": "123.456.789-00"
  }'
```

### **AI Chat**
```bash
curl -X POST https://$FUNCTION_APP_NAME.azurewebsites.net/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Como cadastro uma fazenda?",
    "context": "rural"
  }'
```

---

## 🔥 Executar Fine-Tuning

### **Via GitHub Actions (Recomendado)**

1. Vá para **Actions** no GitHub
2. Execute workflow **Fine-Tuning Pipeline**
3. Preencha:
   - **model_method**: `lora`
   - **dataset_path**: `datasets/train.json`
   - **test_dataset_path**: `datasets/test.json`
   - **deploy_infra**: `true`

### **Via CLI Local**

```bash
# Instalar ModelLab CLI
cd .model_lab/cli
python -m pipx install .

# Adicionar modelo
cd ../../
modellab addModel --model_id microsoft/phi-silica-3.6

# Executar treino
modellab convert --model_id microsoft/phi-silica-3.6 --workflow LoRA
```

---

## 📊 Monitoramento

### **Application Insights**
```bash
# Abrir no portal
az monitor app-insights component show \
  --resource-group rg-ml-finetuning \
  --query id -o tsv | xargs az portal url --destination
```

### **Logs de Fine-Tuning**
```bash
# Logs em tempo real
az containerapp job logs show \
  --name <ACA_JOB_NAME> \
  --resource-group rg-ml-finetuning \
  --follow
```

### **Métricas Cosmos DB**
```bash
az cosmosdb show \
  --resource-group rg-ativoreal-prod \
  --name <COSMOS_ACCOUNT> \
  --query "readLocations[0].documentEndpoint"
```

---

## 🔧 Troubleshooting

### **Fine-Tuning Falha**
```bash
# Ver status do job
az containerapp job execution list \
  --name <ACA_JOB_NAME> \
  --resource-group rg-ml-finetuning

# Ver logs detalhados
az monitor log-analytics query \
  --workspace <LOG_ANALYTICS_ID> \
  --analytics-query "ContainerAppConsoleLogs_CL | where ContainerName_s == 'aiacajoblora' | order by TimeGenerated desc"
```

### **Backend Não Responde**
```bash
# Verificar status
az functionapp show \
  --resource-group rg-ativoreal-prod \
  --name $FUNCTION_APP_NAME \
  --query state

# Ver logs
az functionapp log tail \
  --resource-group rg-ativoreal-prod \
  --name $FUNCTION_APP_NAME
```

### **Cosmos DB Throttling**
```bash
# Aumentar throughput (se não for serverless)
az cosmosdb sql container throughput update \
  --resource-group rg-ativoreal-prod \
  --account-name <COSMOS_ACCOUNT> \
  --database-name AtivoRealDB \
  --name RuralProperties \
  --throughput 4000
```

---

## 💰 Estimativa de Custos (Mensal)

| Recurso | Tier | Custo Estimado |
|---------|------|----------------|
| Cosmos DB Serverless | Pay-per-request | $5-50 |
| Redis Basic C0 | 250MB | $16 |
| Azure Functions Consumption | Pay-per-execution | $5-20 |
| Static Web App Free | Hospedagem | $0 |
| Storage Account Standard LRS | 100GB | $2 |
| Application Insights | 5GB/mês | $0 (free tier) |
| Container Apps GPU A100 | 6h/job | $30-60/job |
| **Total** | - | **$60-150/mês** |

---

## 🎉 Próximos Passos

1. **Treinar primeiro modelo** com dataset de exemplo
2. **Testar chatbot** no frontend
3. **Adicionar autenticação** Azure AD B2C
4. **Implementar PWA** para uso offline
5. **Criar dashboard** de métricas no Power BI

---

## 📝 Comandos Úteis

```bash
# Limpar recursos (cuidado!)
az group delete --name rg-ativoreal-prod --yes --no-wait
az group delete --name rg-ml-finetuning --yes --no-wait

# Ver todos os recursos
az resource list --resource-group rg-ativoreal-prod --output table

# Exportar template atual
az group export \
  --name rg-ativoreal-prod \
  --output json > current-template.json
```

---

**🚀 Tudo pronto! Seu stack está implantado com sucesso.**
