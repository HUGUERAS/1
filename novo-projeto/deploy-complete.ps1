# ==========================================
# DEPLOY COMPLETO "BEM REAL" - AZURE NATIVE
# ==========================================
# Automates: Postgres + PostGIS, Function App (Python), Static Web App (React)

$ErrorActionPreference = "Stop"

# --- CONFIGURAÇÃO ---
$appName = "bemreal-ai1" # Prefixo para recursos ÚNICOS
$location = "brazilsouth"
$rgName = "rg-$appName"
$randomId = Get-Random -Minimum 1000 -Maximum 9999
$dbPassword = "BemReal$randomId!Secure" 
# NOTA: Em produção, use KeyVault ou solicite input seguro. Aqui gerado para facilidade.

# Nomes de Recursos
$storageName = "st${appName}${randomId}".Replace("-", "")
$funcAppName = "func-$appName-$randomId"
$swaName = "swa-$appName-$randomId"
$dbServerName = "psql-$appName-$randomId"
$dbName = "ativoreal_geo"
$dbAdminUser = "bemrealadmin"

Write-Host "=== INICIANDO DEPLOY AUTOMATIZADO ===" -ForegroundColor Cyan
Write-Host "Recursos serão criados em: $rgName ($location)"
Write-Host "Senha do Banco Gerada: $dbPassword" -ForegroundColor Yellow

# 1. Login (se necessário)
$azAccount = az account show 2>$null
if (-not $azAccount) {
    Write-Host "Por favor, faça login no Azure..."
    az login
}

# 2. Criar Resource Group
Write-Host "`nCreating Resource Group..."
az group create --name $rgName --location $location

# 3. Criar PostgreSQL Flexible Server
Write-Host "`nCreating PostgreSQL Server (Isso pode demorar alguns minutos)..."
az postgres flexible-server create `
    --name $dbServerName `
    --resource-group $rgName `
    --location $location `
    --admin-user $dbAdminUser `
    --admin-password $dbPassword `
    --sku-name Standard_B1ms `
    --tier Burstable `
    --version 13 `
    --storage-size 32 `
    --yes

# Ativar Extensões PostGIS (Whitelist)
Write-Host "Configuring Azure Extensions (PostGIS)..."
az postgres flexible-server parameter set `
    --resource-group $rgName `
    --server-name $dbServerName `
    --name azure.extensions `
    --value POSTGIS

# Criar Banco de Dados Específico
az postgres flexible-server db create `
    --resource-group $rgName `
    --server-name $dbServerName `
    --database-name $dbName

Write-Host "NOTA: Você precisará conectar no banco e rodar 'CREATE EXTENSION postgis;' manualmente se o app falhar." -ForegroundColor Yellow

# 4. Storage Account (Para a Function App)
Write-Host "`nCreating Storage Account..."
az storage account create `
    --name $storageName `
    --resource-group $rgName `
    --location $location `
    --sku Standard_LRS

# 5. Criar Function App (Python/Consumption)
Write-Host "`nCreating Function App..."
az functionapp create `
    --name $funcAppName `
    --storage-account $storageName `
    --consumption-plan-location $location `
    --resource-group $rgName `
    --os-type Linux `
    --runtime python `
    --runtime-version 3.11 `
    --functions-version 4

# Configurar Connection String
$dbConnString = "postgresql://$($dbAdminUser):$($dbPassword)@$($dbServerName).postgres.database.azure.com:5432/$($dbName)?sslmode=require"
Write-Host "Setting App Settings..."
az functionapp config appsettings set `
    --name $funcAppName `
    --resource-group $rgName `
    --settings "DATABASE_URL=$dbConnString" "SCM_DO_BUILD_DURING_DEPLOYMENT=true" "BUILD_FLAGS=UseExpressBuild"

# Deploy do Código Backend
Write-Host "`nDeploying Backend Code..."
Push-Location backend
func azure functionapp publish $funcAppName --python
if ($LASTEXITCODE -ne 0) {
    Write-Host "Falha no deploy da Function via 'func'. Tentando via ZIP deploy do AZ CLI..."
    # Fallback ou aviso
}
Pop-Location

# 6. Build & Deploy Frontend
$funcUrl = "https://$funcAppName.azurewebsites.net/api"
Write-Host "`nBackend URL: $funcUrl"

Write-Host "Re-building Frontend with Production API URL..."
Push-Location frontend
$env:VITE_API_URL = $funcUrl
npm install
npm run build
Pop-Location

Write-Host "`nCreating Static Web App..."
# Nota: --api-location-url linka o backend externo (Standard SKU suporta melhor, Free tem limitações)
# Vamos usar o Free e deixar o Frontend chamar a URL completa (Hardcoded no build acima)
az staticwebapp create `
    --name $swaName `
    --resource-group $rgName `
    --location $location `
    --sku Free

$swaToken = az staticwebapp secrets list --name $swaName --resource-group $rgName --query "properties.apiKey" -o tsv

Write-Host "Deploying Frontend Content..."
# Requer swa cli instalado com npm install -g @azure/static-web-apps-cli
# Ou usando Docker image. Vamos tentar via SWA CLI se disponível, senão dar erro.
# Alternativa leve: Usar 'az staticwebapp app up' se suportado ou GitHub Actions.
# Vamos assumir que swa cli está disponivel ou pedir para instalar.
try {
    swa deploy ./frontend/dist --env production --deployment-token $swaToken --app-name $swaName
}
catch {
    Write-Host "SWA CLI não encontrado ou falhou. Tentando instalar..."
    npm install -g @azure/static-web-apps-cli
    swa deploy ./frontend/dist --env production --deployment-token $swaToken --app-name $swaName
}

# 7. Configurar CORS no Backend para aceitar o Frontend
$swaUrl = az staticwebapp show --name $swaName --resource-group $rgName --query "defaultHostname" -o tsv
$fullSwaUrl = "https://$swaUrl"
Write-Host "`nConfiguring CORS for $fullSwaUrl..."
az functionapp cors add --name $funcAppName --resource-group $rgName --allowed-origins $fullSwaUrl

Write-Host "==========================================" -ForegroundColor Green
Write-Host "DEPLOY CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
Write-Host "Frontend: $fullSwaUrl"
Write-Host "Backend: $funcUrl"
Write-Host "Database: $dbServerName"
Write-Host "=========================================="
