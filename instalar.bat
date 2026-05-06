@echo off
title Instalador - Planeador de Rutas

echo ==============================
echo Instalando ambiente del proyecto
echo ==============================

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en PATH.
    echo Instala Python desde https://www.python.org/downloads/
    pause
    exit /b
)

echo Creando ambiente virtual...
python -m venv venv

echo Activando ambiente...
call venv\Scripts\activate

echo Actualizando pip...
python -m pip install --upgrade pip

echo Instalando dependencias...
pip install pandas streamlit folium streamlit-folium requests pyproj

echo.
echo Instalacion completada correctamente.
echo.
pause

