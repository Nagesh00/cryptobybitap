#!/usr/bin/env python3
"""
Test web dashboard startup
"""

print("🌐 Testing Web Dashboard Startup...")

try:
    # Test imports
    print("1. Testing imports...")
    import flask
    import flask_socketio
    print("   ✅ Flask imported")
    
    import os
    if os.path.exists('templates/dashboard.html'):
        print("   ✅ Dashboard template found")
    else:
        print("   ❌ Dashboard template missing")
    
    # Test configuration
    print("2. Testing configuration...")
    import json
    with open('config.json', 'r') as f:
        config = json.load(f)
    print(f"   ✅ Config loaded")
    
    # Test bot components
    print("3. Testing bot components...")
    from utils.logger import setup_logger
    from strategies.moving_average import MovingAverageStrategy
    print("   ✅ Bot components imported")
    
    # Test web dashboard module
    print("4. Testing web dashboard module...")
    import web_dashboard
    print("   ✅ Web dashboard module imported")
    
    print("\n🎉 All tests passed!")
    print("\nTo start the dashboard:")
    print("C:/Users/Nagnath/cryptobybitap/venv/Scripts/python.exe web_dashboard.py")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
    print("\nTroubleshooting steps:")
    print("1. Make sure you're in the correct directory")
    print("2. Check if all files exist")
    print("3. Verify virtual environment is active")
