# ==========================================
# RESUME DEPLOY "BEM REAL" - AZURE NATIVE
# ==========================================
# Script de recuperação para finalizar o deploy usando recursos já criados
# Evita erros de duplicação e foca em enviar o código.

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# --- RECUPERADO DOS LOGS ANTERIORES ---
$appName = "bemreal-ai1"
$rgName = "rg-bemreal-ai1"
$randomId = 1406 # ID gerado na execução anterior
$location = "brazilsouth"
$swaLocation = "eastus2"

# Recriar os nomes exatos
$funcAppName = "func-$appName-$randomId"
$swaName = "swa-$appName-$randomId"
$dbServerName = "psql-$appName-$randomId"

Write-Host "=== RETOMANDO DEPLOY (ID: $randomId) ===" -ForegroundColor Cyan
Write-Host "Usando recursos existentes em: $rgName"

# 1. Deploy Backend (Python)
Write-Host "`n1. Publicando Backend Python (Isso pode levar alguns minutos)..."
Push-Location backend
# Garantir que estamos na pasta certa e publicar
# O comando func exige login, vamos assumir que 'az login' já carrega o contexto ou pedir token
func azure functionapp publish $funcAppName --python
if ($LASTEXITCODE -ne 0) {
    Write-Error "FALHA CRITICA: Não foi possível publicar a Function App."
}
Pop-Location

# 2. Build Frontend (React)
$funcUrl = "https://$funcAppName.azurewebsites.net/api"
Write-Host "`n2. Backend Vivo em: $funcUrl"
Write-Host "Compilando Frontend com essa URL..."

Push-Location ativo-real
$env:VITE_API_URL = $funcUrl
npm install
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Error "FALHA CRITICA: Build do React falhou."
}
Pop-Location

# 3. Deploy Frontend (SWA)
Write-Host "`n3. Enviando Frontend para Azure SWA..."

# Tenta recuperar o token de deploy do recurso já criado
try {
    $swaToken = az staticwebapp secrets list --name $swaName --resource-group $rgName --query "properties.apiKey" -o tsv
} catch {
    Write-Host "Aviso: SWA pode não existir. Tentando criar referência rápida..."
    az staticwebapp create --name $swaName --resource-group $rgName --location $swaLocation --sku Free
    $swaToken = az staticwebapp secrets list --name $swaName --resource-group $rgName --query "properties.apiKey" -o tsv
}

# Deploy via CLI
try {
    swa deploy ./ativo-real/dist --env production --deployment-token $swaToken --app-name $swaName
} catch {
    Write-Host "Instalando SWA CLI..."
    npm install -g @azure/static-web-apps-cli
    swa deploy ./ativo-real/dist --env production --deployment-token $swaToken --app-name $swaName
}

# 4. Configurar CORS (Último passo essencial)
$swaUrl = az staticwebapp show --name $swaName --resource-group $rgName --query "defaultHostname" -o tsv
$fullSwaUrl = "https://$swaUrl"

Write-Host "`n4. Configurando Segurança (CORS) no Backend..."
az functionapp cors add --name $funcAppName --resource-group $rgName --allowed-origins $fullSwaUrl

# RESUMO FINAL
Write-Host "`n==========================================" -ForegroundColor Green
Write-Host "   DEPLOY FINALIZADO COM SUCESSO! 🚀" -ForegroundColor Green
Write-Host "=========================================="
Write-Host "LINK DO SISTEMA: $fullSwaUrl" -ForegroundColor Cyan
Write-Host "API BACKEND:     $funcUrl"
Write-Host "BANCO DE DADOS:  $dbServerName (Postgres)"
Write-Host "=========================================="