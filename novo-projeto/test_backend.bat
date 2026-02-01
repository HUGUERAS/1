@echo off
echo ========================================
echo  INICIANDO TESTES - ATIVO REAL
echo ========================================
echo.

echo [1/4] Verificando Python...
python --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    pause
    exit /b 1
)
echo.

echo [2/4] Verificando dependencias do backend...
cd backend
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
)

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo Instalando dependencias...
pip install -q -r requirements.txt
pip install -q azure-functions
pip install -q geoalchemy2
echo.

echo [3/4] Verificando models...
python -c "import models; print('✓ Models OK')"
if errorlevel 1 (
    echo ERRO: Problema ao importar models!
    pause
    exit /b 1
)
echo.

echo [4/4] Verificando function_app...
python -c "import function_app; print('✓ Function App OK')"
if errorlevel 1 (
    echo ERRO: Problema ao importar function_app!
    pause
    exit /b 1
)
echo.

echo ========================================
echo  TUDO OK! Backend pronto para rodar
echo ========================================
echo.
echo Para iniciar o backend:
echo   cd backend
echo   func start
echo.
echo Para testar os endpoints:
echo   python test_endpoints.py
echo.
pause
