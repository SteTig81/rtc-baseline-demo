
@echo off
if not exist venv (
    where py >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        py -3.14 -m venv venv
    ) else (
        echo ERROR: py.exe is NOT found in the system PATH
        echo HINT: consider to install the Python install manager from https://www.python.org/downloads/
        goto END    
    )
)
call venv\Scripts\activate
python -m pip install --upgrade pip
python main.py --component MyComponent
start python -m http.server 8085
start http://[::1]:8085/
:END
pause
