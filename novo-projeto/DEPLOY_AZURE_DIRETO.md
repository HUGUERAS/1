# 🚀 DEPLOY DIRETO NO AZURE - SEM LOCALHOST

**Para quem não gosta de localhost ou tem problemas com ambiente local**

---

## ✅ PRÉ-REQUISITOS

Antes de começar, você precisa ter:

1. **Conta Azure** ativa
2. **Azure CLI** instalado: <https://aka.ms/azure-cli>
3. **Git** instalado e configurado
4. **GitHub** conta (para CI/CD automático)

---

## 📦 PASSO 1: PREPARAR REPOSITÓRIO GIT

### **1.1 - Inicializar Git (se ainda não tiver)**

```bash
cd c:\Users\User\cooking-agent\ai1.worktrees\copilot-worktree-2026-02-01T05-02-26\novo-projeto

git init
git add .
git commit -m "Implementacao completa - Backend + Frontend MVP"
```

### **1.2 - Criar repositório no GitHub**

1. Acesse: <https://github.com/new>
2. Nome: `ativo-real-topografia`
3. Privado: **Sim** (recomendado)
4. **NÃO** inicialize com README

### **1.3 - Push para GitHub**

```bash
git remote add origin https://github.com/SEU_USUARIO/ativo-real-topografia.git
git branch -M main
git push -u origin main
```

---

## 🗄️ PASSO 2: CRIAR BANCO DE DADOS (PostgreSQL)

### **2.1 - Criar PostgreSQL no Azure**

```bash
# Login no Azure
az login

# Criar Resource Group
az group create \
  --name rg-ativo-real \
  --location brazilsouth

# Criar PostgreSQL Server
az postgres flexible-server create \
  --name ativo-real-db \
  --resource-group rg-ativo-real \
  --location brazilsouth \
  --admin-user adminativo \
  --admin-password "SuaSenhaSegura123!" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 14 \
  --storage-size 32 \
  --public-access 0.0.0.0-255.255.255.255
```

### **2.2 - Criar Database**

```bash
az postgres flexible-server db create \
  --resource-group rg-ativo-real \
  --server-name ativo-real-db \
  --database-name ativo_real
```

### **2.3 - Obter Connection String**

```bash
az postgres flexible-server show-connection-string \
  --server-name ativo-real-db \
  --admin-user adminativo \
  --admin-password "SuaSenhaSegura123!" \
  --database-name ativo_real
```

**Guarde essa string!** Exemplo:

```
postgresql://adminativo:SuaSenhaSegura123!@ativo-real-db.postgres.database.azure.com/ativo_real?sslmode=require
```

---

## 📊 PASSO 3: EXECUTAR SCHEMA SQL

### **Opção A - Via Azure Portal (mais fácil):**

1. Acesse: <https://portal.azure.com>
2. Navegue até: PostgreSQL flexible server → ativo-real-db
3. No menu lateral: **Query editor**
4. Conecte com user/senha
5. Cole o conteúdo de `database/init/05_features_completas.sql`
6. Execute

### **Opção B - Via CLI:**

```bash
# Instalar psql (se não tiver)
# Windows: https://www.postgresql.org/download/windows/

# Conectar e executar
psql "postgresql://adminativo:SuaSenhaSegura123!@ativo-real-db.postgres.database.azure.com/ativo_real?sslmode=require" -f database/init/05_features_completas.sql
```

---

## 🔧 PASSO 4: DEPLOY BACKEND (Azure Functions)

### **4.1 - Criar Function App**

```bash
# Criar Storage Account (necessário para Functions)
az storage account create \
  --name ativorealstorage \
  --resource-group rg-ativo-real \
  --location brazilsouth \
  --sku Standard_LRS

# Criar Function App
az functionapp create \
  --name ativo-real-backend \
  --resource-group rg-ativo-real \
  --consumption-plan-location brazilsouth \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4 \
  --storage-account ativorealstorage \
  --os-type Linux
```

### **4.2 - Configurar Variáveis de Ambiente**

```bash
# Database URL
az functionapp config appsettings set \
  --name ativo-real-backend \
  --resource-group rg-ativo-real \
  --settings "DATABASE_URL=postgresql://adminativo:SuaSenhaSegura123!@ativo-real-db.postgres.database.azure.com/ativo_real?sslmode=require"

# JWT Secret
az functionapp config appsettings set \
  --name ativo-real-backend \
  --resource-group rg-ativo-real \
  --settings "JWT_SECRET=seu_secret_super_seguro_aqui_123456"

# CORS (permitir frontend)
az functionapp cors add \
  --name ativo-real-backend \
  --resource-group rg-ativo-real \
  --allowed-origins "*"
```

### **4.3 - Deploy do Backend**

```bash
cd backend

# Instalar Azure Functions Core Tools (se não tiver)
npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Deploy
func azure functionapp publish ativo-real-backend
```

**✅ Anote a URL do backend:** `https://ativo-real-backend.azurewebsites.net`

---

## 🌐 PASSO 5: DEPLOY FRONTEND (Static Web Apps)

### **5.1 - Criar Static Web App via GitHub Actions**

```bash
az staticwebapp create \
  --name ativo-real-frontend \
  --resource-group rg-ativo-real \
  --source https://github.com/SEU_USUARIO/ativo-real-topografia \
  --location brazilsouth \
  --branch main \
  --app-location "ativo-real" \
  --api-location "backend" \
  --output-location "dist" \
  --login-with-github
```

Este comando vai:

1. Conectar ao seu GitHub
2. Criar um workflow de CI/CD automático
3. Fazer deploy a cada push

### **5.2 - Configurar Variáveis de Ambiente do Frontend**

No Azure Portal:

1. Vá em: Static Web Apps → ativo-real-frontend
2. Configuration → Application settings
3. Adicione:
   - `VITE_API_URL` = `https://ativo-real-backend.azurewebsites.net/api`

### **5.3 - Atualizar API URL no Código**

Edite `ativo-real/src/services/api.ts`:

```typescript
// Trocar:
const API_BASE = '/api';

// Por:
const API_BASE = import.meta.env.VITE_API_URL || '/api';
```

Commit e push:

```bash
git add .
git commit -m "Configure production API URL"
git push
```

**GitHub Actions vai fazer deploy automático!**

---

## ✅ PASSO 6: VERIFICAR DEPLOY

### **6.1 - Obter URLs**

```bash
# URL do Frontend
az staticwebapp show \
  --name ativo-real-frontend \
  --resource-group rg-ativo-real \
  --query "defaultHostname" -o tsv

# URL do Backend
az functionapp show \
  --name ativo-real-backend \
  --resource-group rg-ativo-real \
  --query "defaultHostName" -o tsv
```

### **6.2 - Testar Endpoints**

```bash
# Testar saúde do backend
curl https://ativo-real-backend.azurewebsites.net/api/health

# Testar WMS layers
curl https://ativo-real-backend.azurewebsites.net/api/wms-layers?projeto_id=1
```

---

## 🔐 PASSO 7: CONFIGURAÇÕES DE SEGURANÇA

### **7.1 - Restringir CORS (produção)**

```bash
# Remover "*" e adicionar apenas o domínio do frontend
az functionapp cors remove \
  --name ativo-real-backend \
  --resource-group rg-ativo-real \
  --allowed-origins "*"

az functionapp cors add \
  --name ativo-real-backend \
  --resource-group rg-ativo-real \
  --allowed-origins "https://SEU-FRONTEND.azurestaticapps.net"
```

### **7.2 - Configurar Firewall do PostgreSQL**

```bash
# Permitir apenas Azure Services
az postgres flexible-server firewall-rule create \
  --resource-group rg-ativo-real \
  --name ativo-real-db \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

---

## 📊 PASSO 8: MONITORAMENTO

### **8.1 - Habilitar Application Insights**

```bash
# Criar Application Insights
az monitor app-insights component create \
  --app ativo-real-insights \
  --location brazilsouth \
  --resource-group rg-ativo-real

# Conectar ao Function App
az monitor app-insights component connect-webapp \
  --app ativo-real-insights \
  --resource-group rg-ativo-real \
  --web-app ativo-real-backend
```

### **8.2 - Ver Logs**

```bash
# Logs do Backend
az webapp log tail \
  --name ativo-real-backend \
  --resource-group rg-ativo-real

# Logs do Frontend
az staticwebapp logs show \
  --name ativo-real-frontend \
  --resource-group rg-ativo-real
```

---

## 🎯 RESUMO DAS URLs FINAIS

Após concluir, você terá:

| Serviço | URL |
|---|---|
| **Frontend** | `https://ativo-real-frontend.azurestaticapps.net` |
| **Backend API** | `https://ativo-real-backend.azurewebsites.net/api` |
| **Database** | `ativo-real-db.postgres.database.azure.com` |
| **Portal Azure** | <https://portal.azure.com> |

---

## 💰 CUSTOS ESTIMADOS (MVP)

| Recurso | Plano | Custo/Mês |
|---|---|---|
| PostgreSQL | Standard_B1ms | ~$30 USD |
| Function App | Consumption | ~$0-5 USD |
| Static Web App | Free | $0 USD |
| Storage Account | Standard LRS | ~$1 USD |
| **TOTAL** | | ~$31-36 USD/mês |

---

## 🚀 DEPLOY RÁPIDO (RESUMO)

```bash
# 1. Login
az login

# 2. Criar tudo
az group create --name rg-ativo-real --location brazilsouth
az postgres flexible-server create --name ativo-real-db --resource-group rg-ativo-real ...
az functionapp create --name ativo-real-backend --resource-group rg-ativo-real ...
az staticwebapp create --name ativo-real-frontend --resource-group rg-ativo-real ...

# 3. Deploy backend
cd backend
func azure functionapp publish ativo-real-backend

# 4. Deploy frontend (automático via GitHub Actions)
git push
```

---

## ✅ CHECKLIST DE DEPLOY

- [ ] Repositório no GitHub criado e atualizado
- [ ] Resource Group criado no Azure
- [ ] PostgreSQL criado e configurado
- [ ] Schema SQL executado (05_features_completas.sql)
- [ ] Function App criado e configurado
- [ ] Variáveis de ambiente configuradas
- [ ] Backend deployado (func publish)
- [ ] Static Web App criado
- [ ] GitHub Actions configurado
- [ ] Frontend deployado (automático)
- [ ] CORS configurado
- [ ] Endpoints testados
- [ ] URLs finais anotadas

---

**PRONTO! Seu sistema estará no ar sem precisar de localhost!** 🎉

Para atualizações futuras, basta fazer:

```bash
git add .
git commit -m "Suas alterações"
git push
```

GitHub Actions fará deploy automático! 🚀
