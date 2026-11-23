@echo off
chcp 65001 >nul
echo ===================================================
echo 🛠️  SETUP DE AMBIENTE: STONE SHOP CLONE
echo Autor: Bruno (CTO Uppi)
echo ===================================================
echo.

echo [1/4] Verificando Node.js...
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js não encontrado! Baixe e instale: https://nodejs.org/
    pause
    exit /b 1
) else (
    echo ✅ Node.js instalado!
)

echo.
echo [2/4] Verificando FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ FFmpeg não encontrado no PATH!
    echo    Instalando via winget...
    winget install Gyan.FFmpeg
    echo    Se falhar, instale manualmente de: https://ffmpeg.org/download.html
) else (
    echo ✅ FFmpeg instalado e funcional!
)

echo.
echo [3/4] Instalando dependências npm...
call npm install
echo ✅ Dependências instaladas!

echo.
echo [4/4] Verificando Vercel CLI...
vercel -v >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Vercel CLI não encontrado! Instalando globalmente...
    call npm install -g vercel
) else (
    echo ✅ Vercel CLI pronto!
)

echo.
echo ===================================================
echo 🎉 AMBIENTE 100%% PRONTO PARA USO!
echo Comandos úteis:
echo   npm run dev       -> Inicia o servidor local
echo   npm run sync      -> Sincroniza espelhos e workspace
echo   npm run deploy    -> Faz deploy na Vercel
echo ===================================================
echo.
pause
