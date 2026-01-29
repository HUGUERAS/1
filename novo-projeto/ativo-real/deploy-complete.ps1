#!/usr/bin/env pwsh
# Script de deployment completo - Ativo Real
# Aguarda infraestrutura e publica aplicação

Write-Host "🚀 ATIVO REAL - DEPLOYMENT COMPLETO" -ForegroundColor Cyan
Write-Host "====================================`n" -ForegroundColor Cyan

$resourceGroup = "rg-ativoreal-chile"
$deploymentName = "ativoreal-full-deploy"

# 1. Aguardar conclusão do deployment de infraestrutura
Write-Host "⏳ Aguardando deployment de infraestrutura..." -ForegroundColor Yellow
$maxWaitMinutes = 20
$startTime = Get-Date

while ($true) {
    $deployment = az deployment group show `
        --resource-group $resourceGroup `
        --name $deploymentName `
        --query "properties.provisioningState" `
        --output tsv 2>$null

    $elapsed = [math]::Round(((Get-Date) - $startTime).TotalMinutes, 1)
    
    if ($deployment -eq "Succeeded") {
        Write-Host "✅ Infraestrutura provisionada com sucesso! ($elapsed min)" -ForegroundColor Green
        break
    }
    elseif ($deployment -eq "Failed") {
        Write-Host "❌ Deployment falhou!" -ForegroundColor Red
        az deployment group show --resource-group $resourceGroup --name $deploymentName
        exit 1
    }
    elseif ($elapsed -ge $maxWaitMinutes) {
        Write-Host "⏰ Timeout atingido ($maxWaitMinutes min)" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "  Status: $deployment | Tempo decorrido: $elapsed min" -ForegroundColor Gray
    Start-Sleep -Seconds 30
}

# 2. Capturar outputs do deployment
Write-Host "`n📋 Capturando outputs..." -ForegroundColor Yellow
$outputs = az deployment group show `
    --resource-group $resourceGroup `
    --name $deploymentName `
    --query "properties.outputs" | ConvertFrom-Json

$functionAppName = $outputs.functionAppName.value
$staticWebAppName = $outputs.staticWebAppName.value
$cosmosEndpoint = $outputs.cosmosDbEndpoint.value
$cosmosKey = $outputs.cosmosDbKey.value
$redisConnectionString = $outputs.redisConnectionString.value
$appInsightsConnectionString = $outputs.appInsightsConnectionString.value

Write-Host "  Function App: $functionAppName" -ForegroundColor Cyan
Write-Host "  Static Web App: $staticWebAppName" -ForegroundColor Cyan
Write-Host "  Cosmos DB Endpoint: $cosmosEndpoint" -ForegroundColor Cyan

# 3. Configurar variáveis de ambiente no Function App
Write-Host "`n⚙️  Configurando variáveis de ambiente..." -ForegroundColor Yellow
az functionapp config appsettings set `
    --name $functionAppName `
    --resource-group $resourceGroup `
    --settings `
        "COSMOS_ENDPOINT=$cosmosEndpoint" `
        "COSMOS_KEY=$cosmosKey" `
        "REDIS_CONNECTION_STRING=$redisConnectionString" `
        "APPLICATIONINSIGHTS_CONNECTION_STRING=$appInsightsConnectionString" `
        "ENABLE_ORYX_BUILD=true" `
        "SCM_DO_BUILD_DURING_DEPLOYMENT=true" | Out-Null

Write-Host "✅ Variáveis configuradas" -ForegroundColor Green

# 4. Publicar Azure Functions
Write-Host "`n📦 Publicando Azure Functions..." -ForegroundColor Yellow
Push-Location api

# Renomear function_app_cosmosdb.py para function_app.py
if (Test-Path "function_app_cosmosdb.py") {
    Write-Host "  Usando function_app_cosmosdb.py como função principal..." -ForegroundColor Gray
    Copy-Item "function_app_cosmosdb.py" "function_app.py" -Force
}

func azure functionapp publish $functionAppName --python

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Functions publicadas com sucesso!" -ForegroundColor Green
} else {
    Write-Host "❌ Erro ao publicar Functions" -ForegroundColor Red
    Pop-Location
    exit 1
}

Pop-Location

# 5. Build do frontend
Write-Host "`n🏗️  Building frontend..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Build concluído!" -ForegroundColor Green
} else {
    Write-Host "❌ Erro no build" -ForegroundColor Red
    exit 1
}

# 6. Deploy do Static Web App
Write-Host "`n🌐 Deploying Static Web App..." -ForegroundColor Yellow
$deploymentToken = az staticwebapp secrets list `
    --name $staticWebAppName `
    --resource-group $resourceGroup `
    --query "properties.apiKey" `
    --output tsv

az staticwebapp upload `
    --name $staticWebAppName `
    --resource-group $resourceGroup `
    --deployment-token $deploymentToken `
    --app-location "." `
    --output-location "dist" | Out-Null

Write-Host "✅ Static Web App deployed!" -ForegroundColor Green

# 7. Teste dos endpoints
Write-Host "`n🧪 Testando endpoints..." -ForegroundColor Yellow
$functionUrl = "https://$functionAppName.azurewebsites.net"
$staticUrl = az staticwebapp show `
    --name $staticWebAppName `
    --resource-group $resourceGroup `
    --query "defaultHostname" `
    --output tsv

Write-Host "`n  Aguardando Functions ficarem online..." -ForegroundColor Gray
Start-Sleep -Seconds 60

try {
    $healthResponse = Invoke-RestMethod -Uri "$functionUrl/api/health" -Method Get -TimeoutSec 10
    Write-Host "  ✅ Health Check: OK" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  Health Check: Aguarde alguns minutos para Functions inicializarem" -ForegroundColor Yellow
}

# 8. Resumo final
Write-Host "`n" -NoNewline
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎉 DEPLOYMENT CONCLUÍDO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`n📍 URLs da aplicação:" -ForegroundColor Yellow
Write-Host "  Frontend: https://$staticUrl" -ForegroundColor Cyan
Write-Host "  API:      $functionUrl/api" -ForegroundColor Cyan
Write-Host "`n📊 Monitoramento:" -ForegroundColor Yellow
Write-Host "  Application Insights: Portal Azure > $resourceGroup > AppInsights" -ForegroundColor Cyan
Write-Host "`n🔧 Próximos passos:" -ForegroundColor Yellow
Write-Host "  1. Configure PHI_SILICA_ENDPOINT e PHI_SILICA_API_KEY no Function App" -ForegroundColor White
Write-Host "  2. Teste o chatbot AI em: https://$staticUrl" -ForegroundColor White
Write-Host "  3. Monitore logs em Application Insights" -ForegroundColor White
Write-Host "`n" -NoNewline
