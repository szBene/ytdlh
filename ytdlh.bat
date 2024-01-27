@echo off
setlocal

:: Get the directory of the batch file
set "script_dir=%~dp0"

:: call ytdlh.exe and pass all arguments
%script_dir%\ytdlh\ytdlh.exe %*

endlocal
