@echo off
setlocal

::set current dorectory
set "output_name=ytdlh"

:: Get the directory of the batch file
set "script_dir=%~dp0"

:: Run the pyinstaller command
pyinstaller -c --name %output_name% main.py ytdlp_handler.py

:: Check if the pyinstaller command is executed successfully
if ERRORLEVEL 0 (
    echo Successfully built %output_name%. Finishing up...
    copy %script_dir%ytdlh.bat %script_dir%dist
    powershell Compress-Archive -Force -Path "%script_dir%dist\*" -DestinationPath %script_dir%ytdlh-build.zip

    rmdir /s /q %script_dir%dist
    rmdir /s /q %script_dir%build
    del /q %script_dir%%output_name%.spec
    echo The finished build is located at %script_dir%ytdlh-build.zip
)

endlocal
