@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo Hermes Premium - Inicializador Portavel
echo ========================================
echo.

if not exist "venv\Scripts\python.exe" (
    echo Criando ambiente virtual local...
    py -3 -m venv venv
    if errorlevel 1 (
        echo.
        echo Nao foi possivel criar o ambiente virtual com "py -3".
        echo Tente instalar Python 3.10+ ou rode: python -m venv venv
        pause
        exit /b 1
    )
)

echo Instalando/atualizando dependencias...
"venv\Scripts\python.exe" -m pip install --upgrade pip
"venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Falha ao instalar dependencias. Verifique a internet e tente novamente.
    pause
    exit /b 1
)

echo.
echo Iniciando Hermes Premium em http://127.0.0.1:8000
echo Usuario inicial: admin
echo Senha inicial: admin123
echo.
start "" "http://127.0.0.1:8000"
"venv\Scripts\python.exe" -m uvicorn api:app --host 127.0.0.1 --port 8000

pause
