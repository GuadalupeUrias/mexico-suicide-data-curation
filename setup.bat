@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM Setup automático del entorno del proyecto (Windows)
REM Detecta Python; si no existe, lo instala solo via winget.
REM ============================================================

echo ==^> Verificando si Python esta instalado...

where python >nul 2>nul
if %errorlevel% equ 0 (
    set PYCMD=python
    goto :python_found
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    set PYCMD=py
    goto :python_found
)

echo Python no fue encontrado. Intentando instalar automaticamente con winget...
where winget >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo No se encontro winget en este equipo.
    echo Instala Python manualmente desde https://python.org/downloads
    echo IMPORTANTE: en el instalador, marca la casilla "Add python.exe to PATH".
    echo Luego vuelve a correr este script: setup.bat
    pause
    exit /b 1
)

winget install --id Python.Python.3.12 -e --silent --accept-package-agreements --accept-source-agreements
if %errorlevel% neq 0 (
    echo.
    echo La instalacion automatica fallo. Instala Python manualmente desde https://python.org/downloads
    echo IMPORTANTE: marca "Add python.exe to PATH" en el instalador.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Python fue instalado correctamente.
echo Windows necesita que CIERRES y vuelvas a abrir la terminal
echo para reconocer el nuevo PATH (esto es una limitacion de Windows,
echo no del script).
echo.
echo Pasos:
echo   1. Cierra esta terminal
echo   2. Abre una terminal nueva en la carpeta del proyecto
echo   3. Vuelve a correr: setup.bat
echo ============================================================
pause
exit /b 0

:python_found
echo Python encontrado: usando comando "%PYCMD%"
%PYCMD% --version

echo ==^> Creando entorno virtual (venv)...
%PYCMD% -m venv venv
if not exist venv\Scripts\activate.bat (
    echo.
    echo No se pudo crear el entorno virtual. Verifica tu instalacion de Python.
    pause
    exit /b 1
)

echo ==^> Activando entorno virtual e instalando dependencias...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ==^> Registrando kernel de Jupyter para este proyecto...
python -m ipykernel install --user --name=mexico-suicide-data-curation --display-name "Python (mexico-suicide-data-curation)"

echo.
echo ============================================================
echo Listo. Entorno configurado correctamente.
echo Pasos siguientes:
echo   1. Abre el proyecto en VS Code: code .
echo   2. Instala las extensiones recomendadas cuando aparezca el aviso.
echo   3. Abre un notebook en notebooks/ y selecciona el kernel
echo      "Python (mexico-suicide-data-curation)".
echo ============================================================
pause
