#!/usr/bin/env python3
"""
Launch the Bybit Trading Bot Web Dashboard
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading

def open_browser():
    """Open browser after a delay"""
    time.sleep(5)
    print("🌐 Opening web browser...")
    webbrowser.open('http://localhost:5000')

def main():
    print("🚀 BYBIT TRADING BOT WEB DASHBOARD")
    print("=" * 50)
    print("📊 Dashboard Features:")
    print("  ✅ Real-time account balance")
    print("  ✅ Live trading signals") 
    print("  ✅ Position tracking")
    print("  ✅ Price charts with moving averages")
    print("  ✅ Trading history")
    print("  ✅ Bot status monitoring")
    print()
    print("🌐 Dashboard URL: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    # Get the correct Python executable
    if os.path.exists('venv/Scripts/python.exe'):
        python_exe = 'venv/Scripts/python.exe'
    elif os.path.exists('venv/bin/python'):
        python_exe = 'venv/bin/python'
    else:
        python_exe = sys.executable
    
    print(f"📍 Using Python: {python_exe}")
    
    # Start browser opening thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        print("\n🔄 Starting web dashboard server...")
        # Run the web dashboard
        result = subprocess.run([python_exe, "web_dashboard.py"], 
                              capture_output=False, 
                              text=True)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Dashboard stopped by user")
    except FileNotFoundError:
        print(f"\n❌ Error: Could not find Python executable at {python_exe}")
        print("Try running: python web_dashboard.py")
    except Exception as e:
        print(f"\n❌ Error starting dashboard: {e}")
        print("\nTroubleshooting:")
        print("1. Check if virtual environment is set up:")
        print("   python -m venv venv")
        print("2. Install dependencies:")
        print("   pip install -r requirements.txt")
        print("   pip install -r web_requirements.txt")
        print("3. Check config.json exists")
        print("4. Try direct command:")
        print("   python web_dashboard.py")

if __name__ == "__main__":
    main()
