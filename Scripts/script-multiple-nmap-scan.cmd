@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION
SETLOCAL

SET script=%~0
FOR %%k IN ("%script%") DO (
SET scriptdrive=%%~dk
SET scriptpath=%%~pk
SET scriptname=%%~nk
SET scriptextension=%%~xk
)

SET file=%~1
FOR %%i IN ("%file%") DO (
SET filedrive=%%~di
SET filepath=%%~pi
SET filename=%%~ni
SET fileextension=%%~xi
)


for /f %%j in (%file%) do (
    nmap -Pn -sSV -p- -sC -T4 --stats-every 10s --script-timeout 1000ms --host-timeout 120m -oA %filedrive%%filepath%%%j %%j 
)


