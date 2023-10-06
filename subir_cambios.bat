@echo off
echo Realizando commit y pull en GitHub...

rem Cambia al directorio de tu repositorio
cd /d "G:\Proyectos_GitHub\ScanRemoteConnections"

rem Agrega todos los archivos modificados al área de preparación
git add .

rem Realiza el commit sin un mensaje específico
git commit -m "Actualización automática"

rem Realiza un pull para asegurarte de tener la última versión de la rama "main"
git pull origin main

rem Empuja los cambios a la rama "main" en el repositorio remoto
git push origin main

echo Commit y pull completados.

pause