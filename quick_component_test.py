#!/usr/bin/env python3
"""
Quick test to verify bot components work
"""

def test_imports():
    print("Testing imports...")
    try:
        import pandas as pd
        import numpy as np
        from pybit.unified_trading import HTTP
        from utils.logger import setup_logger
        from strategies.moving_average import MovingAverageStrategy
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    print("Testing configuration...")
    try:
        import json
        with open('config.json', 'r') as f:
            config = json.load(f)
        print(f"✅ Config loaded - API Key: {config['api_key'][:10]}...")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_strategy():
    print("Testing strategy...")
    try:
        from strategies.moving_average import MovingAverageStrategy
        import numpy as np
        
        strategy = MovingAverageStrategy()
        
        # Create simple test data
        sample_data = {
            'result': {
                'list': [
                    ['1640000000000', '50000', '51000', '49000', '50500', '1000'],
                    ['1640000060000', '50500', '51500', '49500', '51000', '1000'],
                    ['1640000120000', '51000', '52000', '50000', '51500', '1000']
                ]
            }
        }
        
        signal, ma_short, ma_long = strategy.get_current_signal(sample_data)
        print(f"✅ Strategy works - Signal: {signal or 'HOLD'}")
        return True
    except Exception as e:
        print(f"❌ Strategy error: {e}")
        return False

def test_web_components():
    print("Testing web components...")
    try:
        import flask
        import flask_socketio
        print("✅ Flask components available")
        
        # Test template exists
        import os
        if os.path.exists('templates/dashboard.html'):
            print("✅ Dashboard template found")
            return True
        else:
            print("❌ Dashboard template missing")
            return False
    except Exception as e:
        print(f"❌ Web component error: {e}")
        return False

def main():
    print("🔍 QUICK COMPONENT TEST")
    print("=" * 30)
    
    tests = [
        test_imports,
        test_config,
        test_strategy,
        test_web_components
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All components working!")
        print("\nReady to run:")
        print("• Web Dashboard: python start_dashboard.py")
        print("• Command Line: python bot.py")
    else:
        print("⚠️  Some issues found - check above")

if __name__ == "__main__":
    main()
