#!/usr/bin/env python3
"""
Launch the Bybit Trading Bot Web Dashboard
"""

import subprocess
import sys
import webbrowser
import time
import threading

def open_browser():
    """Open browser after a delay"""
    time.sleep(3)
    print("Opening web browser...")
    webbrowser.open('http://localhost:5000')

def main():
    print("🚀 Starting Bybit Trading Bot Web Dashboard...")
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
    
    # Start browser opening thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        # Run the web dashboard
        subprocess.run([sys.executable, "web_dashboard.py"])
    except KeyboardInterrupt:
        print("\n\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting dashboard: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have installed web dependencies:")
        print("   pip install -r web_requirements.txt")
        print("2. Check if port 5000 is available")
        print("3. Verify your config.json file exists")

if __name__ == "__main__":
    main()
