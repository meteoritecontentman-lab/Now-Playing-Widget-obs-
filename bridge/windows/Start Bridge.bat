@echo off
cd /d "%~dp0"
title Now Playing Bridge

echo ==============================================
echo   Now Playing Bridge - Windows
echo ==============================================
echo.

where python >nul 2>&1
if errorlevel 1 (
  echo Python not found. Install from https://python.org
  echo Enable "Add Python to PATH" during setup.
  pause
  exit /b 1
)

if not exist "venv" (
  echo First run - setting up...
  python -m venv venv
  call venv\Scripts\activate.bat
  python -m pip install --upgrade pip
  pip install flask flask-cors winsdk
  echo Setup complete.
  echo.
) else (
  call venv\Scripts\activate.bat
)

echo Starting bridge... Leave this window open while streaming.
echo.
python server.py
pause
