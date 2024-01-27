@echo off
setlocal

:: If the script is run with a parameter (drag and drop), use that as the zip file
:: Otherwise, use 'ytdlh-build.zip' in the current directory
if "%~1"=="" (set "zipFile=ytdlh-build.zip") else (set "zipFile=%~1")

:: Set the destination to the current user's home directory
set "destination=C:\Users\%USERNAME%"

:: Delete the existing files, if any
del /f /q "%destination%\ytdlh.bat"
rd /s /q "%destination%\ytdlh"

:: Extract the zip file
tar -xf "%zipFile%" -C "%destination%"

if ERRORLEVEL 0 (
    echo Successfully installed ytdlh to "%destination%"
) else (
    echo Failed to install ytdlh to "%destination%"
)

:: user input before exiting
pause

endlocal
