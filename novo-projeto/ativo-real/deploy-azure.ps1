# ==========================================
# DEPLOY ATIVO REAL NO AZURE - CLI DIRETO
# ==========================================
# Execute linha por linha no PowerShell

# 1. LOGIN NO AZURE
az login

# 2. DEFINIR VARIÁVEIS
$resourceGroup = "rg-ativo-real"
$location = "brazilsouth"
$staticWebAppName = "swa-ativo-real"
$functionAppName = "func-ativo-real"
$storageName = "stativorealprod"  # Somente letras minúsculas e números
$dbServerName = "psql-ativo-real"
$dbName = "ativo_real_db"
$dbAdminUser = "ativorealadmin"
$dbAdminPassword = "SuaSenhaSegura123!"  # TROCAR ISSO!

# 3. CRIAR RESOURCE GROUP
az group create `
  --name $resourceGroup `
  --location $location

# 4. CRIAR AZURE STATIC WEB APP (Frontend)
az staticwebapp create `
  --name $staticWebAppName `
  --resource-group $resourceGroup `
  --location $location `
  --sku Free

# 5. CRIAR STORAGE ACCOUNT (Para Functions)
az storage account create `
  --name $storageName `
  --resource-group $resourceGroup `
  --location $location `
  --sku Standard_LRS

# 6. CRIAR POSTGRESQL FLEXIBLE SERVER
az postgres flexible-server create `
  --name $dbServerName `
  --resource-group $resourceGroup `
  --location $location `
  --admin-user $dbAdminUser `
  --admin-password $dbAdminPassword `
  --sku-name Standard_B1ms `
  --tier Burstable `
  --version 14 `
  --storage-size 32 `
  --public-access 0.0.0.0-255.255.255.255

# 7. CRIAR DATABASE
az postgres flexible-server db create `
  --resource-group $resourceGroup `
  --server-name $dbServerName `
  --database-name $dbName

# 8. CRIAR AZURE FUNCTION APP (Python 3.11)
az functionapp create `
  --name $functionAppName `
  --resource-group $resourceGroup `
  --storage-account $storageName `
  --runtime python `
  --runtime-version 3.11 `
  --functions-version 4 `
  --os-type Linux `
  --consumption-plan-location $location

# 9. CONFIGURAR CONNECTION STRING DO POSTGRESQL
$connectionString = "dbname=$dbName user=$dbAdminUser password=$dbAdminPassword host=$dbServerName.postgres.database.azure.com sslmode=require"

az functionapp config appsettings set `
  --name $functionAppName `
  --resource-group $resourceGroup `
  --settings "POSTGRES_CONNECTION_STRING=$connectionString"

# 10. BUILD DO FRONTEND
cd C:\Users\huugo\topdemais\ativo-real
npm install
npm run build

# 11. OBTER TOKEN DA STATIC WEB APP
$swaToken = az staticwebapp secrets list `
  --name $staticWebAppName `
  --resource-group $resourceGroup `
  --query properties.apiKey `
  --output tsv

Write-Host "Token da Static Web App: $swaToken" -ForegroundColor Green

# 12. DEPLOY DO FRONTEND (usando SWA CLI)
npx @azure/static-web-apps-cli deploy `
  --app-location . `
  --output-location dist `
  --api-location api `
  --deployment-token $swaToken

# 13. DEPLOY DO BACKEND (Azure Functions)
cd api
func azure functionapp publish $functionAppName --python

# 14. OBTER URLS DE PRODUÇÃO
$swaUrl = az staticwebapp show `
  --name $staticWebAppName `
  --resource-group $resourceGroup `
  --query defaultHostname `
  --output tsv

$funcUrl = az functionapp show `
  --name $functionAppName `
  --resource-group $resourceGroup `
  --query defaultHostName `
  --output tsv

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ DEPLOY CONCLUÍDO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Frontend: https://$swaUrl" -ForegroundColor Yellow
Write-Host "Backend:  https://$funcUrl" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan
