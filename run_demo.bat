
@echo off
rem If a working venv already exists, reuse it. Otherwise create a new one.
if exist venv\Scripts\python.exe (
	echo Found existing venv, reusing it.
) else (
	echo Creating new virtual environment 'venv' with Python 3.14...
	rem Ensure the py launcher can provide Python 3.14; abort if not present
	py -3.14 -V >nul 2>&1 && (
		py -3.14 -m venv venv
	) || (
		echo ERROR: 'py -3.14' is not available or failed to run.
		echo Please install Python 3.14 and ensure the py launcher supports '-3.14',
		echo or create the virtualenv manually and re-run this script.
		exit /b 1
	)
)

call venv\Scripts\activate
python -m pip install --upgrade pip
rem python generate_samples.py
python main.py --component MyComponent
python -m http.server 8080
pause
