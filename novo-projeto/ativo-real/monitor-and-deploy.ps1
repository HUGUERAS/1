#!/usr/bin/env pwsh
# Monitor e auto-executa deployment completo

$resourceGroup = "rg-ativoreal-chile"
$deploymentName = "ativoreal-full-deploy"

Write-Host "🔍 Monitorando deployment..." -ForegroundColor Cyan

while ($true) {
    Start-Sleep -Seconds 15
    
    $status = az deployment group show `
        --resource-group $resourceGroup `
        --name $deploymentName `
        --query "properties.provisioningState" `
        --output tsv 2>$null
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    
    if ($status -eq "Succeeded") {
        Write-Host "[$timestamp] ✅ Deploy concluído!" -ForegroundColor Green
        Write-Host "`n🚀 Iniciando publicação da aplicação..." -ForegroundColor Yellow
        & "c:\Users\huugo\topdemais\ativo-real\deploy-complete.ps1"
        break
    }
    elseif ($status -eq "Failed") {
        Write-Host "[$timestamp] ❌ Deploy falhou!" -ForegroundColor Red
        az deployment group show --resource-group $resourceGroup --name $deploymentName
        break
    }
    else {
        Write-Host "[$timestamp] ⏳ Status: $status" -ForegroundColor Gray
    }
}
