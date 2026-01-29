Write-Host "=== CONFIGURAÇÃO DE AMBIENTE ===" -ForegroundColor Cyan

# 1. Tentar instalar Azure CLI via WinGet
try {
    Write-Host "Tentando instalar Azure CLI via WinGet..."
    winget install -e --id Microsoft.AzureCLI --accept-source-agreements --accept-package-agreements
} catch {
    Write-Host "Erro ao usar WinGet para Azure CLI." -ForegroundColor Yellow
}

# 2. Tentar instalar Func Core Tools via NPM (já tentado pelo agente, mas reforçando)
try {
    Write-Host "Tentando instalar Func Core Tools via NPM..."
    npm install -g azure-functions-core-tools@4
} catch {
    Write-Host "Erro ao usar NPM." -ForegroundColor Yellow
}

# 3. Verificação Final e Instruções Manuais
Write-Host "`n=== VERIFICAÇÃO ===" -ForegroundColor Cyan
$azInstalled = Get-Command az -ErrorAction SilentlyContinue
$funcInstalled = Get-Command func -ErrorAction SilentlyContinue

if ($azInstalled) { Write-Host "✅ Azure CLI encontrado." -ForegroundColor Green }
else { 
    Write-Host "❌ Azure CLI NÃO encontrado." -ForegroundColor Red
    Write-Host "Baixe e instale manualmente: https://aka.ms/installazurecliwindows"
}

if ($funcInstalled) { Write-Host "✅ Azure Functions Core Tools encontrado." -ForegroundColor Green }
else {
    Write-Host "❌ Func Tools NÃO encontrado." -ForegroundColor Red
    Write-Host "Baixe e instale manualmente: https://go.microsoft.com/fwlink/?linkid=2174087"
}

Write-Host "`nApós instalar, FECHE e REABRA este terminal, depois rode: ./deploy-complete.ps1" -ForegroundColor Cyan
