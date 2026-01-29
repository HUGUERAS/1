# 🚀 DEPLOY RÁPIDO NO AZURE - PASSO A PASSO

## Pré-requisitos

```powershell
# Instalar Azure CLI
winget install Microsoft.AzureCLI

# Instalar Azure Functions Core Tools
npm install -g azure-functions-core-tools@4

# Instalar SWA CLI
npm install -g @azure/static-web-apps-cli
```

## Opção 1: Deploy Automático (Recomendado)

```powershell
cd C:\Users\huugo\topdemais\ativo-real

# Edite deploy-azure.ps1 e troque a senha do PostgreSQL
notepad deploy-azure.ps1

# Execute o script completo
.\deploy-azure.ps1
```

## Opção 2: Deploy Manual (Comandos Individuais)

### 1️⃣ Login
```powershell
az login
```

### 2️⃣ Criar Resource Group
```powershell
az group create --name rg-ativo-real --location brazilsouth
```

### 3️⃣ Criar Static Web App
```powershell
az staticwebapp create `
  --name swa-ativo-real `
  --resource-group rg-ativo-real `
  --location brazilsouth `
  --sku Free
```

### 4️⃣ Build Frontend
```powershell
cd C:\Users\huugo\topdemais\ativo-real
npm install
npm run build
```

### 5️⃣ Deploy Frontend
```powershell
# Obter token
$token = az staticwebapp secrets list `
  --name swa-ativo-real `
  --resource-group rg-ativo-real `
  --query properties.apiKey `
  --output tsv

# Deploy
npx @azure/static-web-apps-cli deploy `
  --app-location . `
  --output-location dist `
  --api-location api `
  --deployment-token $token
```

### 6️⃣ Criar PostgreSQL (Opcional - se precisar do backend)
```powershell
az postgres flexible-server create `
  --name psql-ativo-real `
  --resource-group rg-ativo-real `
  --location brazilsouth `
  --admin-user ativorealadmin `
  --admin-password "SuaSenhaSegura123!" `
  --sku-name Standard_B1ms `
  --tier Burstable `
  --public-access 0.0.0.0-255.255.255.255
```

### 7️⃣ Deploy Backend (Opcional)
```powershell
# Criar Function App
az functionapp create `
  --name func-ativo-real `
  --resource-group rg-ativo-real `
  --storage-account stativorealprod `
  --runtime python `
  --runtime-version 3.11 `
  --functions-version 4 `
  --os-type Linux `
  --consumption-plan-location brazilsouth

# Deploy
cd api
func azure functionapp publish func-ativo-real --python
```

## 🎯 Opção 3: Deploy ULTRA RÁPIDO (Só Frontend)

Se você quer testar **SEM backend** primeiro:

```powershell
# 1. Login
az login

# 2. Criar tudo de uma vez
az staticwebapp create `
  --name swa-ativo-real `
  --resource-group rg-ativo-real `
  --location brazilsouth `
  --sku Free

# 3. Build
cd C:\Users\huugo\topdemais\ativo-real
npm install
npm run build

# 4. Deploy
$token = az staticwebapp secrets list --name swa-ativo-real --resource-group rg-ativo-real --query properties.apiKey -o tsv
npx @azure/static-web-apps-cli deploy --output-location dist --deployment-token $token

# 5. Abrir no navegador
az staticwebapp show --name swa-ativo-real --resource-group rg-ativo-real --query defaultHostname -o tsv
```

## 📊 Custos Estimados

| Recurso | Tier | Custo/Mês |
|---------|------|-----------|
| Static Web App | Free | R$ 0 |
| Functions (Consumption) | Pay-per-use | ~R$ 5-20 |
| PostgreSQL (B1ms) | Burstable | ~R$ 50-80 |

**Total estimado:** R$ 0-100/mês dependendo do uso

## 🔧 Troubleshooting

### Erro: "az command not found"
```powershell
# Reinicie o PowerShell após instalar Azure CLI
```

### Erro: "npm command not found"
```powershell
# Instale Node.js primeiro
winget install OpenJS.NodeJS
```

### Deploy trava ou falha
```powershell
# Limpe cache e tente novamente
npm run build
Remove-Item -Recurse -Force dist
npm run build
```

## 🌐 URLs Após Deploy

Seu site estará em:
```
https://swa-ativo-real-XXXXXXXX.azurestaticapps.net
```

Backend (se configurado):
```
https://func-ativo-real.azurewebsites.net
```

## 🔄 Updates Futuros

Para atualizar o site depois de fazer mudanças:

```powershell
# Build
npm run build

# Deploy
$token = az staticwebapp secrets list --name swa-ativo-real --resource-group rg-ativo-real --query properties.apiKey -o tsv
npx @azure/static-web-apps-cli deploy --output-location dist --deployment-token $token
```
