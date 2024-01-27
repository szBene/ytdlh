@echo off
setlocal

:: Set the destination to the current user's home directory
set "destination=C:\Users\%USERNAME%"

:: Delete the existing files, if any
del /f /q "%destination%\ytdlh.bat"
rd /s /q "%destination%\ytdlh"

echo Successfully uninstalled ytdlh from "%destination%"

:: user input before exiting
pause

endlocal
