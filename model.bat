@echo off
REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.x before running this program.
    pause
    exit /B 1
)

REM Check if pip is installed
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip is not installed. Please install pip before running this program.
    pause
    exit /B 1
)

REM Create virtual environment if it does not exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

echo Installing required packages...
pip install -r requirements.txt

echo Starting the program...
python pngtuber.py > log.txt 2>&1