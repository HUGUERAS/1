@echo off
title ATIVO REAL - Iniciar Tudo
color 0A

echo.
echo  ╔════════════════════════════════════════════════════════════╗
echo  ║                                                            ║
echo  ║              🚀 ATIVO REAL - INICIAR TUDO 🚀               ║
echo  ║                                                            ║
echo  ║              Sistema de Topografia SaaS                    ║
echo  ║              Versao: MVP 1.0                               ║
echo  ║                                                            ║
echo  ╚════════════════════════════════════════════════════════════╝
echo.
echo.

echo [PASSO 1/5] Verificando ambiente...
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python NAO encontrado! Instale Python 3.9+
    pause
    exit /b 1
)
echo ✓ Python instalado

REM Verificar Node
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js NAO encontrado! Instale Node.js 18+
    pause
    exit /b 1
)
echo ✓ Node.js instalado

REM Verificar PostgreSQL
psql --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PostgreSQL nao encontrado (opcional para testes locais)
) else (
    echo ✓ PostgreSQL instalado
)

echo.
echo [PASSO 2/5] Preparando Backend...
echo.

cd backend

if not exist "venv" (
    echo Criando ambiente virtual Python...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Instalando dependencias do backend...
pip install -q -r requirements.txt
pip install -q azure-functions geoalchemy2

echo ✓ Backend preparado!

cd ..

echo.
echo [PASSO 3/5] Preparando Frontend...
echo.

cd ativo-real

if not exist "node_modules" (
    echo Instalando dependencias do frontend...
    call npm install
) else (
    echo ✓ Dependencias ja instaladas
)

echo ✓ Frontend preparado!

cd ..

echo.
echo [PASSO 4/5] Executando testes basicos...
echo.

echo Testando imports do backend...
cd backend
call venv\Scripts\activate.bat
python -c "import models; print('✓ Models OK')" 2>nul
if errorlevel 1 (
    echo ⚠️  Aviso: Problema ao importar models
)

python -c "import function_app; print('✓ Function App OK')" 2>nul
if errorlevel 1 (
    echo ⚠️  Aviso: Problema ao importar function_app
)

cd ..

echo.
echo Verificando componentes do frontend...
if exist "ativo-real\src\components\ClientForm.tsx" (
    echo ✓ ClientForm.tsx
)
if exist "ativo-real\src\components\ChatWidget.tsx" (
    echo ✓ ChatWidget.tsx
)
if exist "ativo-real\src\components\StatusTimeline.tsx" (
    echo ✓ StatusTimeline.tsx
)

echo.
echo [PASSO 5/5] Abrindo terminais...
echo.

echo Abrindo terminal para o BACKEND...
start "BACKEND - Azure Functions" cmd /k "cd backend && call venv\Scripts\activate.bat && echo Backend rodando em http://localhost:7071 && func start"

timeout /t 3 /nobreak >nul

echo Abrindo terminal para o FRONTEND...
start "FRONTEND - Vite Dev Server" cmd /k "cd ativo-real && echo Frontend rodando em http://localhost:5173 && npm run dev"

timeout /t 2 /nobreak >nul

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                    ✅ TUDO INICIADO!                       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Aguarde alguns segundos para os servicos iniciarem...
echo.
echo 📊 URLS:
echo    Backend:  http://localhost:7071
echo    Frontend: http://localhost:5173
echo.
echo 📝 PROXIMOS PASSOS:
echo    1. Aguarde o backend iniciar (≈30 segundos)
echo    2. Aguarde o frontend compilar (≈10 segundos)
echo    3. Abra http://localhost:5173 no navegador
echo    4. Execute: python test_endpoints.py (para testar API)
echo.
echo 📖 DOCUMENTACAO:
echo    - GUIA_TESTE_RAPIDO.md
echo    - IMPLEMENTACAO_FINAL_COMPLETA.md
echo    - CHECKLIST_FINAL_DEPLOY.md
echo.
echo ⚠️  Para parar os servicos: Feche as janelas de terminal
echo.
pause
