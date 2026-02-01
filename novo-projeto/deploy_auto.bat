@echo off
title DEPLOY AUTOMATICO - Ativo Real
color 0A

echo.
echo  ================================================================
echo   DEPLOY 100%% AUTOMATICO - ATIVO REAL
echo  ================================================================
echo.

REM 1. PRE-REQUISITOS
echo [1/8] Verificando pre-requisitos...
call az --version >nul 2>&1
if errorlevel 1 ( echo Azure CLI nao instalado. & pause & exit /b 1 )
call git --version >nul 2>&1
if errorlevel 1 ( echo Git nao instalado. & pause & exit /b 1 )
call node --version >nul 2>&1
if errorlevel 1 ( echo Node.js nao instalado. & pause & exit /b 1 )
echo OK.

REM 2. LOGIN
echo.
echo [2/8] Login no Azure...
echo ⚠️  Uma janela do navegador vai abrir. Faca o login!
call az login
if errorlevel 1 ( echo Falha no login. & pause & exit /b 1 )
echo OK.

REM 3. RESOURCE GROUP
echo.
echo [3/8] Resource Group (rg-ativo-real)...
call az group create --name rg-ativo-real --location brazilsouth
if errorlevel 1 ( echo Falha ao criar RG. & pause & exit /b 1 )
echo OK.

REM 4. POSTGRESQL
echo.
echo [4/8] PostgreSQL...
echo Buscando servidor existente ou criando novo...
echo.

REM Tenta pegar existente primeiro
for /f "tokens=*" %%i in ('az postgres flexible-server list --resource-group rg-ativo-real --query "[0].name" -o tsv 2^>nul') do set POSTGRES_NAME=%%i

if "%POSTGRES_NAME%"=="" (
    echo Nenhum servidor encontrado. Criando novo...
    call az postgres flexible-server create ^
      --name ativo-real-db-%RANDOM% ^
      --resource-group rg-ativo-real ^
      --location brazilsouth ^
      --admin-user adminativo ^
      --admin-password "AtivO@Real2026!" ^
      --sku-name Standard_B1ms ^
      --tier Burstable ^
      --version 14 ^
      --storage-size 32 ^
      --public-access 0.0.0.0-255.255.255.255 ^
      --yes

    if errorlevel 1 ( echo Falha ao criar PostgreSQL. & pause & exit /b 1 )
    
    REM Pega o nome do que acabou de criar
    for /f "tokens=*" %%i in ('az postgres flexible-server list --resource-group rg-ativo-real --query "[0].name" -o tsv') do set POSTGRES_NAME=%%i
) else (
    echo Usando servidor existente: %POSTGRES_NAME%
)

echo.
echo Criando Database 'ativo_real' se nao existir...
call az postgres flexible-server db create --resource-group rg-ativo-real --server-name %POSTGRES_NAME% --database-name ativo_real
echo OK.

REM 5. SETUP DB (O PULO DO GATO)
echo.
echo [5/8] Configurando tabelas do Banco de Dados (AUTOMATICO)...
echo Instalando driver postgres...
call pip install psycopg2-binary
echo Rodando script Python de deploy...
python deploy_db.py %POSTGRES_NAME% adminativo "AtivO@Real2026!" ativo_real
if errorlevel 1 ( echo Erro no setup do DB. & pause & exit /b 1 )
echo OK.

REM 6. FUNCTION APP
echo.
echo [6/8] Function App...
echo Buscando Storage...
for /f "tokens=*" %%i in ('az storage account list --resource-group rg-ativo-real --query "[0].name" -o tsv 2^>nul') do set STORAGE_NAME=%%i

if "%STORAGE_NAME%"=="" (
    call az storage account create --name ativorealstore%RANDOM% --resource-group rg-ativo-real --location brazilsouth --sku Standard_LRS
    for /f "tokens=*" %%i in ('az storage account list --resource-group rg-ativo-real --query "[0].name" -o tsv') do set STORAGE_NAME=%%i
)
echo Storage: %STORAGE_NAME%

echo Buscando Function App...
for /f "tokens=*" %%i in ('az functionapp list --resource-group rg-ativo-real --query "[0].name" -o tsv 2^>nul') do set FUNCTION_NAME=%%i

if "%FUNCTION_NAME%"=="" (
    call az functionapp create ^
      --name ativo-real-api-%RANDOM% ^
      --resource-group rg-ativo-real ^
      --consumption-plan-location brazilsouth ^
      --runtime python ^
      --runtime-version 3.9 ^
      --functions-version 4 ^
      --storage-account %STORAGE_NAME% ^
      --os-type Linux

    for /f "tokens=*" %%i in ('az functionapp list --resource-group rg-ativo-real --query "[0].name" -o tsv') do set FUNCTION_NAME=%%i
)
echo App: %FUNCTION_NAME%

REM 7. VARIAVEIS
echo.
echo [7/8] Configurando variaveis...
call az functionapp config appsettings set --name %FUNCTION_NAME% --resource-group rg-ativo-real --settings "DATABASE_URL=postgresql://adminativo:AtivO@Real2026!@%POSTGRES_NAME%.postgres.database.azure.com/ativo_real?sslmode=require" "JWT_SECRET=super_secret_auto_deploy"
call az functionapp cors add --name %FUNCTION_NAME% --resource-group rg-ativo-real --allowed-origins "*"
echo OK.

REM 8. DEPLOY CODE
echo.
echo [8/8] Publicando codigo Python...
cd backend
call func azure functionapp publish %FUNCTION_NAME% --build remote
cd ..

echo.
echo  ================================================================
echo   ✅ SUCESSO! DEPLOY FINALIZADO
echo  ================================================================
echo.
echo  API URL: https://%FUNCTION_NAME%.azurewebsites.net/api
echo.
pause
