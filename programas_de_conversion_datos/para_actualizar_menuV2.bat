@echo off

REM Verificar si PyInstaller está instalado
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller no está instalado. Instalando...
    pip install pyinstaller
) else (
    echo PyInstaller ya está instalado.
)

REM Cambiar al directorio de trabajo
cd C:\Users\Francisco\Desktop\programas_de_conversion_datos

REM Compilar el programa Python con PyInstaller
pyinstaller --onefile C:\Users\Francisco\Desktop\programas_de_conversion_datos\pasaje_codigos_numeracion_menuV2.py

REM Pausa para ver cualquier mensaje de salida
pause