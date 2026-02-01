#!/usr/bin/env powershell
# Deploy script para backend do Ativo Real

Write-Host "========================================" -ForegroundColor Green
Write-Host "🚀 ATIVO REAL Backend Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# 1. Check if func CLI is installed
Write-Host "✅ Checking Azure Functions CLI..." -ForegroundColor Yellow
$funcVersion = func --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   Found: $funcVersion" -ForegroundColor Green
} else {
    Write-Host "   ❌ Azure Functions CLI not found!" -ForegroundColor Red
    Write-Host "   Install: npm install -g azure-functions-core-tools@4 --unsafe-perm true" -ForegroundColor Yellow
    exit 1
}

# 2. Check if requirements are installed
Write-Host ""
Write-Host "✅ Checking Python dependencies..." -ForegroundColor Yellow
$pythonPath = $env:PYTHON_ENV_PATH
if (-not $pythonPath) {
    $pythonPath = (python -c "import sys; print(sys.executable)" 2>&1)
}
Write-Host "   Python: $pythonPath" -ForegroundColor Green

# 3. Show what we're deploying
Write-Host ""
Write-Host "📦 Deployment Configuration:" -ForegroundColor Cyan
Write-Host "   Function App: swa-ativo-real" -ForegroundColor White
Write-Host "   Backend Location: novo-projeto/backend" -ForegroundColor White
Write-Host "   Endpoints: 50+ (Auth, Projects, Lots, Payments, Chat, WMS)" -ForegroundColor White
Write-Host ""

# 4. Deploy
Write-Host "🎯 Starting deployment..." -ForegroundColor Yellow
Write-Host ""

cd "c:\Users\User\cooking-agent\ai1\novo-projeto\backend"
Write-Host "   Working directory: $(Get-Location)" -ForegroundColor Gray

# Run deployment with verbose output
Write-Host "   Executing: func azure functionapp publish swa-ativo-real --build remote" -ForegroundColor Gray
Write-Host ""

func azure functionapp publish swa-ativo-real --build remote

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📍 Backend URL: https://swa-ativo-real.azurestaticapps.net/api/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Available endpoints:" -ForegroundColor Yellow
    Write-Host "   POST   /api/auth/login" -ForegroundColor White
    Write-Host "   GET    /api/projects" -ForegroundColor White
    Write-Host "   POST   /api/projects" -ForegroundColor White
    Write-Host "   GET    /api/lots/{lot_id}" -ForegroundColor White
    Write-Host "   POST   /api/payments" -ForegroundColor White
    Write-Host "   GET    /api/wms-layers" -ForegroundColor White
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Test login endpoint:" -ForegroundColor White
    Write-Host "      curl -X POST https://swa-ativo-real.azurestaticapps.net/api/auth/login" -ForegroundColor Gray
    Write-Host "      -H 'Content-Type: application/json'" -ForegroundColor Gray
    Write-Host '      -d ''{"email":"topografo@bemreal.com","password":"password"}''' -ForegroundColor Gray
    Write-Host ""
    Write-Host "   2. Deploy frontend React app" -ForegroundColor White
    Write-Host "   3. Test full workflow" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "❌ DEPLOYMENT FAILED!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "   1. Check if logged in: az account show" -ForegroundColor White
    Write-Host "   2. Check requirements: pip install -r requirements.txt" -ForegroundColor White
    Write-Host "   3. Check logs: func azure functionapp log tail swa-ativo-real" -ForegroundColor White
    exit 1
}
