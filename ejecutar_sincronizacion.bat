@echo off
setlocal
:: Cambiar al directorio del proyecto
cd /d "D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast"

:: Activar el entorno virtual y ejecutar el script
echo [%date% %time%] Iniciando sincronizacion de lanzamientos... >> sync_log.txt
call .\venv\Scripts\activate
python .\launch\sync_launches_historical.py >> sync_log.txt 2>&1

:: Desactivar venv (opcional en un .bat que termina)
call deactivate
echo [%date% %time%] Sincronizacion finalizada. >> sync_log.txt
echo ------------------------------------------ >> sync_log.txt
endlocal
