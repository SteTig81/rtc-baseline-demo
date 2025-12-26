
@echo off
py -3.14 -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
rem python generate_samples.py
python main.py --component MyComponent
python -m http.server 8080
pause
