#!/usr/bin/env python3
"""
Simple Web Dashboard Test
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

try:
    print("🌐 Starting Bybit Trading Bot Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    # Import and run web dashboard
    from web_dashboard import app, socketio, bot_interface
    
    # Start monitoring
    bot_interface.start_monitoring()
    
    # Run the app
    socketio.run(app, host='127.0.0.1', port=5000, debug=False, allow_unsafe_werkzeug=True)
    
except KeyboardInterrupt:
    print("\n🛑 Dashboard stopped")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install flask flask-socketio")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Check if config.json exists and all files are present")
