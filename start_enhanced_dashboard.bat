@echo off
echo 🚀 Starting Enhanced Bybit Trading Dashboard...
echo ================================================
echo.
cd /d "C:\Users\Nagnath\cryptobybitap"
echo 📍 Current directory: %CD%
echo.
echo 🔧 Activating virtual environment...
call "C:\Users\Nagnath\cryptobybitap\venv\Scripts\activate.bat"
echo.
echo 📊 Starting enhanced trading dashboard...
echo 🌐 Dashboard will be available at: http://localhost:5000
echo 💼 Features: Real-time trading, live charts, position management
echo.
"C:\Users\Nagnath\cryptobybitap\venv\Scripts\python.exe" enhanced_web_dashboard.py
echo.
echo ⏹️ Dashboard stopped. Press any key to exit...
pause
