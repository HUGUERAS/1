@echo off
echo ========================================
echo  INICIANDO TESTES - FRONTEND
echo ========================================
echo.

echo [1/3] Verificando Node.js...
node --version
if errorlevel 1 (
    echo ERRO: Node.js nao encontrado!
    pause
    exit /b 1
)
echo.

echo [2/3] Verificando npm...
npm --version
if errorlevel 1 (
    echo ERRO: npm nao encontrado!
    pause
    exit /b 1
)
echo.

cd ativo-real

echo [3/3] Verificando dependencias...
if not exist "node_modules" (
    echo Instalando dependencias do frontend...
    call npm install
)
echo.

echo ========================================
echo  Verificando componentes criados...
echo ========================================

if exist "src\components\ClientForm.tsx" (
    echo ✓ ClientForm.tsx
) else (
    echo ✗ ClientForm.tsx NAO ENCONTRADO
)

if exist "src\components\ChatWidget.tsx" (
    echo ✓ ChatWidget.tsx
) else (
    echo ✗ ChatWidget.tsx NAO ENCONTRADO
)

if exist "src\components\StatusTimeline.tsx" (
    echo ✓ StatusTimeline.tsx
) else (
    echo ✗ StatusTimeline.tsx NAO ENCONTRADO
)

if exist "src\components\FileUploader.tsx" (
    echo ✓ FileUploader.tsx
) else (
    echo ✗ FileUploader.tsx NAO ENCONTRADO
)

if exist "src\components\WMSLayerManager.tsx" (
    echo ✓ WMSLayerManager.tsx
) else (
    echo ✗ WMSLayerManager.tsx NAO ENCONTRADO
)

if exist "src\components\ContractViewer.tsx" (
    echo ✓ ContractViewer.tsx
) else (
    echo ✗ ContractViewer.tsx NAO ENCONTRADO
)

if exist "src\components\ClientPortal.tsx" (
    echo ✓ ClientPortal.tsx
) else (
    echo ✗ ClientPortal.tsx NAO ENCONTRADO
)

echo.
echo ========================================
echo  FRONTEND PRONTO!
echo ========================================
echo.
echo Para iniciar o dev server:
echo   cd ativo-real
echo   npm run dev
echo.
echo Depois acesse:
echo   http://localhost:5173
echo.
pause
