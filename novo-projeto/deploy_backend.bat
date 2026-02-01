@echo off
title DEPLOY AZURE - Ativo Real
color 0B

echo.
echo  ╔════════════════════════════════════════════════════════════╗
echo  ║                                                            ║
echo  ║           🚀 DEPLOY AUTOMATICO - ATIVO REAL 🚀             ║
echo  ║                                                            ║
echo  ║              Sistema de Topografia SaaS                    ║
echo  ║              Deploy direto no Azure                        ║
echo  ║                                                            ║
echo  ╚════════════════════════════════════════════════════════════╝
echo.
echo.

REM ============================================
REM PASSO 1: VERIFICAR PRE-REQUISITOS
REM ============================================

echo [PASSO 1/8] Verificando pre-requisitos...
echo.

REM Verificar Azure CLI
az --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Azure CLI NAO encontrado!
    echo.
    echo Por favor, instale Azure CLI:
    echo https://aka.ms/azure-cli
    echo.
    pause
    exit /b 1
)
echo ✓ Azure CLI instalado

REM Verificar Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git NAO encontrado!
    echo.
    echo Por favor, instale Git:
    echo https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)
echo ✓ Git instalado

REM Verificar Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js NAO encontrado!
    echo.
    echo Por favor, instale Node.js:
    echo https://nodejs.org
    echo.
    pause
    exit /b 1
)
echo ✓ Node.js instalado

echo.
echo ════════════════════════════════════════════════════════════
echo  PRE-REQUISITOS OK!
echo ════════════════════════════════════════════════════════════
echo.
pause

REM ============================================
REM PASSO 2: LOGIN NO AZURE
REM ============================================

echo.
echo [PASSO 2/8] Fazendo login no Azure...
echo.

az login

if errorlevel 1 (
    echo ❌ Erro ao fazer login no Azure!
    pause
    exit /b 1
)

echo ✓ Login bem-sucedido!
echo.
pause

REM ============================================
REM PASSO 3: CRIAR RESOURCE GROUP
REM ============================================

echo.
echo [PASSO 3/8] Criando Resource Group...
echo.

az group create --name rg-ativo-real --location brazilsouth

if errorlevel 1 (
    echo ❌ Erro ao criar Resource Group!
    echo Talvez ja exista. Continuando...
)

echo ✓ Resource Group criado/existente!
echo.
pause

REM ============================================
REM PASSO 4: CRIAR POSTGRESQL
REM ============================================

echo.
echo [PASSO 4/8] Criando PostgreSQL Server...
echo ⏳ Isso pode levar 3-5 minutos. Aguarde...
echo.

az postgres flexible-server create ^
  --name ativo-real-db-%RANDOM% ^
  --resource-group rg-ativo-real ^
  --location brazilsouth ^
  --admin-user adminativo ^
  --admin-password "AtivO@Real2026!" ^
  --sku-name Standard_B1ms ^
  --tier Burstable ^
  --version 14 ^
  --storage-size 32 ^
  --public-access 0.0.0.0-255.255.255.255

if errorlevel 1 (
    echo.
    echo ❌ Erro ao criar PostgreSQL!
    echo.
    echo SOLUCAO:
    echo 1. Tente outro nome (adicione numeros)
    echo 2. Ou use Azure Portal: https://portal.azure.com
    echo.
    pause
    exit /b 1
)

echo ✓ PostgreSQL criado!
echo.

REM Pegar o nome do servidor
for /f "tokens=*" %%i in ('az postgres flexible-server list --resource-group rg-ativo-real --query "[0].name" -o tsv') do set POSTGRES_NAME=%%i

echo Nome do servidor: %POSTGRES_NAME%
echo.

REM Criar database
echo Criando database 'ativo_real'...
az postgres flexible-server db create ^
  --resource-group rg-ativo-real ^
  --server-name %POSTGRES_NAME% ^
  --database-name ativo_real

echo ✓ Database criado!
echo.
pause

REM ============================================
REM PASSO 5: EXECUTAR SQL
REM ============================================

echo.
echo [PASSO 5/8] Executar Schema SQL
echo.
echo ⚠️  IMPORTANTE: Voce precisa executar o SQL manualmente!
echo.
echo 1. Acesse: https://portal.azure.com
echo 2. Busque: %POSTGRES_NAME%
echo 3. Menu: Databases ^> ativo_real
echo 4. Menu: Query editor
echo 5. Login: adminativo / AtivO@Real2026!
echo 6. Cole o conteudo de: database\init\05_features_completas.sql
echo 7. Execute
echo.
echo Pressione qualquer tecla APOS executar o SQL...
pause

REM ============================================
REM PASSO 6: CRIAR FUNCTION APP
REM ============================================

echo.
echo [PASSO 6/8] Criando Function App...
echo.

REM Storage Account
echo Criando Storage Account...
az storage account create ^
  --name ativorealstorage%RANDOM% ^
  --resource-group rg-ativo-real ^
  --location brazilsouth ^
  --sku Standard_LRS

if errorlevel 1 (
    echo ❌ Erro ao criar Storage Account!
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('az storage account list --resource-group rg-ativo-real --query "[0].name" -o tsv') do set STORAGE_NAME=%%i

echo ✓ Storage Account criado: %STORAGE_NAME%
echo.

REM Function App
echo Criando Function App...
az functionapp create ^
  --name ativo-real-backend-%RANDOM% ^
  --resource-group rg-ativo-real ^
  --consumption-plan-location brazilsouth ^
  --runtime python ^
  --runtime-version 3.9 ^
  --functions-version 4 ^
  --storage-account %STORAGE_NAME% ^
  --os-type Linux

if errorlevel 1 (
    echo ❌ Erro ao criar Function App!
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('az functionapp list --resource-group rg-ativo-real --query "[0].name" -o tsv') do set FUNCTION_NAME=%%i

echo ✓ Function App criado: %FUNCTION_NAME%
echo.
pause

REM ============================================
REM PASSO 7: CONFIGURAR VARIAVEIS
REM ============================================

echo.
echo [PASSO 7/8] Configurando variaveis de ambiente...
echo.

REM Database URL
az functionapp config appsettings set ^
  --name %FUNCTION_NAME% ^
  --resource-group rg-ativo-real ^
  --settings "DATABASE_URL=postgresql://adminativo:AtivO@Real2026!@%POSTGRES_NAME%.postgres.database.azure.com/ativo_real?sslmode=require"

REM JWT Secret
az functionapp config appsettings set ^
  --name %FUNCTION_NAME% ^
  --resource-group rg-ativo-real ^
  --settings "JWT_SECRET=ativo_real_jwt_secret_2026_super_secure"

REM CORS
az functionapp cors add ^
  --name %FUNCTION_NAME% ^
  --resource-group rg-ativo-real ^
  --allowed-origins "*"

echo ✓ Variaveis configuradas!
echo.
pause

REM ============================================
REM PASSO 8: DEPLOY BACKEND
REM ============================================

echo.
echo [PASSO 8/8] Fazendo deploy do backend...
echo ⏳ Isso pode levar 2-3 minutos...
echo.

cd backend

REM Verificar se tem Azure Functions Core Tools
func --version >nul 2>&1
if errorlevel 1 (
    echo Azure Functions Core Tools nao encontrado!
    echo Instalando...
    call npm install -g azure-functions-core-tools@4 --unsafe-perm true
)

REM Deploy
func azure functionapp publish %FUNCTION_NAME% --build remote

if errorlevel 1 (
    echo ❌ Erro no deploy!
    cd ..
    pause
    exit /b 1
)

cd ..

echo.
echo ════════════════════════════════════════════════════════════
echo  ✅ DEPLOY DO BACKEND CONCLUIDO!
echo ════════════════════════════════════════════════════════════
echo.
echo 🔗 URL do Backend:
echo https://%FUNCTION_NAME%.azurewebsites.net/api
echo.
echo.

REM Salvar informacoes
echo # INFORMACOES DO DEPLOY > DEPLOY_INFO.txt
echo. >> DEPLOY_INFO.txt
echo Data: %DATE% %TIME% >> DEPLOY_INFO.txt
echo. >> DEPLOY_INFO.txt
echo Resource Group: rg-ativo-real >> DEPLOY_INFO.txt
echo PostgreSQL: %POSTGRES_NAME% >> DEPLOY_INFO.txt
echo Database: ativo_real >> DEPLOY_INFO.txt
echo User: adminativo >> DEPLOY_INFO.txt
echo Password: AtivO@Real2026! >> DEPLOY_INFO.txt
echo. >> DEPLOY_INFO.txt
echo Storage: %STORAGE_NAME% >> DEPLOY_INFO.txt
echo Function App: %FUNCTION_NAME% >> DEPLOY_INFO.txt
echo. >> DEPLOY_INFO.txt
echo Backend URL: https://%FUNCTION_NAME%.azurewebsites.net/api >> DEPLOY_INFO.txt
echo. >> DEPLOY_INFO.txt

echo ✓ Informacoes salvas em: DEPLOY_INFO.txt
echo.
echo.
echo ════════════════════════════════════════════════════════════
echo  📝 PROXIMOS PASSOS:
echo ════════════════════════════════════════════════════════════
echo.
echo 1. ✅ Backend deployado com sucesso!
echo.
echo 2. 🌐 Deploy do Frontend:
echo    - Crie repositorio no GitHub
echo    - Execute: deploy_frontend.bat
echo.
echo 3. 🧪 Testar endpoints:
echo    curl https://%FUNCTION_NAME%.azurewebsites.net/api/wms-layers?projeto_id=1
echo.
echo 4. 📊 Ver logs no Azure Portal:
echo    https://portal.azure.com
echo.
echo ════════════════════════════════════════════════════════════
echo.
pause

REM Abrir Azure Portal
echo Deseja abrir o Azure Portal para ver os recursos? (S/N)
set /p OPEN_PORTAL=
if /i "%OPEN_PORTAL%"=="S" (
    start https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups
)

echo.
echo ✅ DEPLOY CONCLUIDO!
echo.
pause
