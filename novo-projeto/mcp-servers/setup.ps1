# Script de Configuração Automática - MCP Ativo Real
# Autor: Hugo Cardoso
# Data: Janeiro 2026

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MCP Ativo Real - Configurador" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 1. Verificar Node.js
Write-Host "[1/6] Verificando Node.js..." -ForegroundColor Yellow
$nodeVersion = node --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: Node.js nao instalado! Baixe em: https://nodejs.org" -ForegroundColor Red
    exit 1
}
Write-Host "OK: Node.js $nodeVersion encontrado" -ForegroundColor Green

# 2. Compilar servidores
Write-Host "`n[2/6] Compilando servidores MCP..." -ForegroundColor Yellow
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: Falha na compilacao!" -ForegroundColor Red
    exit 1
}
Write-Host "OK: Servidores compilados em dist/" -ForegroundColor Green

# 3. Localizar config do Claude
Write-Host "`n[3/6] Localizando Claude Desktop..." -ForegroundColor Yellow
$claudeConfigPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$claudeConfigDir = "$env:APPDATA\Claude"

if (-not (Test-Path $claudeConfigDir)) {
    Write-Host "AVISO: Pasta do Claude nao encontrada!" -ForegroundColor Yellow
    Write-Host "Criando: $claudeConfigDir" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $claudeConfigDir -Force | Out-Null
}

Write-Host "OK: $claudeConfigPath" -ForegroundColor Green

# 4. Backup do config existente
if (Test-Path $claudeConfigPath) {
    Write-Host "`n[4/6] Fazendo backup do config existente..." -ForegroundColor Yellow
    $backupPath = "$claudeConfigPath.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item $claudeConfigPath $backupPath
    Write-Host "OK: Backup salvo em: $backupPath" -ForegroundColor Green
} else {
    Write-Host "`n[4/6] Nenhum config existente encontrado" -ForegroundColor Yellow
}

# 5. Criar configuração
Write-Host "`n[5/6] Gerando claude_desktop_config.json..." -ForegroundColor Yellow

$currentDir = (Get-Location).Path
$filesystemPath = Join-Path $currentDir "dist\filesystem-server.js"
$cosmosdbPath = Join-Path $currentDir "dist\cosmosdb-server.js"

# Converter para formato JSON com barras escapadas
$filesystemPathJson = $filesystemPath -replace '\\', '\\'
$cosmosdbPathJson = $cosmosdbPath -replace '\\', '\\'

$config = @{
    mcpServers = @{
        "ativo-real-filesystem" = @{
            command = "node"
            args = @($filesystemPathJson)
        }
        "ativo-real-cosmosdb" = @{
            command = "node"
            args = @($cosmosdbPathJson)
            env = @{
                COSMOS_ENDPOINT = "https://SEU-COSMOS-ACCOUNT.documents.azure.com:443/"
                COSMOS_KEY = "SUA-CHAVE-PRIMARIA-AQUI"
            }
        }
    }
}

$configJson = $config | ConvertTo-Json -Depth 10
$configJson | Set-Content -Path $claudeConfigPath -Encoding UTF8

Write-Host "OK: Configuracao criada!" -ForegroundColor Green

# 6. Instruções finais
Write-Host "`n[6/6] Proximos passos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. COSMOS DB (OBRIGATORIO para MCP Cosmos DB):" -ForegroundColor Cyan
Write-Host "   - Acesse: https://portal.azure.com" -ForegroundColor White
Write-Host "   - Va em Azure Cosmos DB > Keys" -ForegroundColor White
Write-Host "   - Copie URI e Primary Key" -ForegroundColor White
Write-Host "   - Edite: $claudeConfigPath" -ForegroundColor White
Write-Host "   - Substitua SEU-COSMOS-ACCOUNT e SUA-CHAVE-PRIMARIA" -ForegroundColor White
Write-Host ""
Write-Host "2. REINICIAR Claude Desktop" -ForegroundColor Cyan
Write-Host "   - Feche completamente (Ctrl+Q ou Task Manager)" -ForegroundColor White
Write-Host "   - Abra novamente" -ForegroundColor White
Write-Host ""
Write-Host "3. TESTAR:" -ForegroundColor Cyan
Write-Host '   Digite no Claude: "Liste os arquivos em C:\Users"' -ForegroundColor White
Write-Host ""
Write-Host "Configuracao salva em:" -ForegroundColor Green
Write-Host "  $claudeConfigPath" -ForegroundColor White
Write-Host ""
Write-Host "Documentacao completa:" -ForegroundColor Green
Write-Host "  CONFIGURACAO.md" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Configuracao concluida!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
