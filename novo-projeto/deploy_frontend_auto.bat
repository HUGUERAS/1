@echo off
title DEPLOY FRONTEND - Ativo Real
color 0D

echo.
echo  ================================================================
echo   DEPLOY FRONTEND AUTOMATICO - ATIVO REAL
echo  ================================================================
echo.

REM Verificar pré-requisitos básicos
call az --version >nul 2>&1
if errorlevel 1 ( echo Azure CLI nao instalado. & pause & exit /b 1 )
call node --version >nul 2>&1
if errorlevel 1 ( echo Node.js nao instalado. & pause & exit /b 1 )
call swa --version >nul 2>&1
if errorlevel 1 ( 
    echo SWA CLI nao instalado. Instalando...
    call npm install -g @azure/static-web-apps-cli
)

echo Executando script de deploy Python...
python deploy_frontend.py

echo.
pause
