@echo off
echo Starting Bybit Trading Bot Web Dashboard...
echo.
cd /d "C:\Users\Nagnath\cryptobybitap"
echo Current directory: %CD%
echo.
echo Activating virtual environment...
call "C:\Users\Nagnath\cryptobybitap\venv\Scripts\activate.bat"
echo.
echo Starting web dashboard...
"C:\Users\Nagnath\cryptobybitap\venv\Scripts\python.exe" web_dashboard.py
pause
