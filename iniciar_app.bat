@echo off
title Iniciar Planeador de Rutas

cd /d "%~dp0"

echo Iniciando servidor local...
echo Abriendo navegador...

start http://localhost:8000

python -m http.server 8000

pause