@echo off
REM Script para abrir varios archivos .exe con argumentos

REM Lanzar auto.exe con los argumentos especificados
start "" "C:\meta\autoMetaFX.exe" -s EURUSD -t 1H -b 100 -l 0.01
start "" "C:\meta\autoMetaFX.exe" -s USDJPY -t 30M -b 100 -l 0.01
start "" "C:\meta\autoMetaFX.exe" -s GBPUSD -t 4H -b 100 -l 0.01
start "" "C:\meta\autoMetaFX.exe" -s USDMXN -t 4H -b 100 -l 0.01
start "" "C:\meta\autoMetaFX.exe" -s EURJPY -t 4H -b 100 -l 0.01
start "" "C:\meta\autoMetaFX.exe" -s CADJPY -t 4H -b 100 -l 0.01
start "" "C:\meta\autoMetaFX.exe" -s EURCAD -t 4H -b 100 -l 0.01
start "" "C:\meta\autoMetaFX.exe" -s OILCash -t 4H -b 100 -l 0.01
start "" "C:\meta\autoMetaFX.exe" -s NGASCash -t 4H -b 100 -l 0.01

REM Puedes agregar tantas líneas como necesites para abrir otros archivos .exe con sus respectivos argumentos

echo Todos los archivos .exe se han lanzado.
pause
