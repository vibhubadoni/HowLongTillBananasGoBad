@echo off
setlocal
cd /d "%~dp0"

echo ===========================================
echo       🍌 Banana AI - Starting...
echo ===========================================
echo.

if not exist ".venv\Scripts\activate.bat" (
    echo [Error] Virtual environment not found. Please ensure dependencies are installed.
    pause
    exit /b
)

call .venv\Scripts\activate

:: Check if Streamlit is installed
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo [Setup] Streamlit not found. Installing...
    pip install streamlit
)

echo [Launch] Starting Streamlit App...
streamlit run app.py
pause
