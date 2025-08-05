#!/usr/bin/env python3
"""
Debug script for the Bybit trading bot
Tests individual components without requiring API keys
"""

import sys
import traceback
import pandas as pd
import numpy as np
from datetime import datetime

def test_imports():
    """Test all imports"""
    print("Testing imports...")
    try:
        # Test standard library imports
        import json
        import time
        import os
        print("✓ Standard library imports successful")
        
        # Test third-party imports
        import pandas as pd
        import numpy as np
        print("✓ Pandas and NumPy imports successful")
        
        from pybit.unified_trading import HTTP
        print("✓ PyBit import successful")
        
        # Test local imports
        from utils.logger import setup_logger
        print("✓ Logger import successful")
        
        from strategies.moving_average import MovingAverageStrategy
        print("✓ Strategy import successful")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        traceback.print_exc()
        return False

def test_logger():
    """Test logging functionality"""
    print("\nTesting logger...")
    try:
        from utils.logger import setup_logger
        logger = setup_logger("test_logger")
        logger.info("Test log message")
        print("✓ Logger working correctly")
        return True
    except Exception as e:
        print(f"✗ Logger error: {e}")
        traceback.print_exc()
        return False

def test_strategy():
    """Test moving average strategy with sample data"""
    print("\nTesting strategy...")
    try:
        from strategies.moving_average import MovingAverageStrategy
        
        # Create sample market data
        sample_data = {
            'result': {
                'list': []
            }
        }
        
        # Generate 100 sample klines (timestamp, open, high, low, close, volume)
        base_price = 50000
        for i in range(100):
            timestamp = int(datetime.now().timestamp() * 1000) - (99-i) * 60000
            price = base_price + np.random.normal(0, 100)  # Random walk
            sample_data['result']['list'].append([
                str(timestamp),
                str(price - np.random.uniform(0, 50)),  # open
                str(price + np.random.uniform(0, 100)), # high
                str(price - np.random.uniform(0, 100)), # low
                str(price),                             # close
                str(np.random.uniform(1000, 10000))     # volume
            ])
        
        strategy = MovingAverageStrategy(short_period=20, long_period=50)
        signal, ma_short, ma_long = strategy.get_current_signal(sample_data)
        
        print(f"✓ Strategy test successful")
        print(f"  Signal: {signal}")
        print(f"  MA Short: {ma_short:.2f}" if ma_short else "  MA Short: None")
        print(f"  MA Long: {ma_long:.2f}" if ma_long else "  MA Long: None")
        
        return True
    except Exception as e:
        print(f"✗ Strategy error: {e}")
        traceback.print_exc()
        return False

def test_config_loading():
    """Test configuration loading"""
    print("\nTesting config loading...")
    try:
        import json
        
        # Test loading config file
        with open('config.json', 'r') as file:
            config = json.load(file)
        
        print("✓ Config file loaded successfully")
        print(f"  Trading pairs: {config.get('trading_pairs', [])}")
        print(f"  Testnet: {config.get('testnet', True)}")
        print(f"  MA periods: {config.get('ma_short_period', 20)}/{config.get('ma_long_period', 50)}")
        
        # Check for placeholder values
        if config.get('api_key') == 'YOUR_BYBIT_API_KEY_HERE':
            print("⚠ Warning: API key still has placeholder value")
        if config.get('api_secret') == 'YOUR_BYBIT_API_SECRET_HERE':
            print("⚠ Warning: API secret still has placeholder value")
        
        return True
    except Exception as e:
        print(f"✗ Config loading error: {e}")
        traceback.print_exc()
        return False

def test_bot_class():
    """Test bot class initialization (without API calls)"""
    print("\nTesting bot class...")
    try:
        # Import the bot class
        from bot import BybitTradingBot
        
        # We can't actually initialize it without valid API keys
        # But we can test the class exists and methods are defined
        required_methods = [
            'load_config', 'initialize_client', 'get_account_balance',
            'get_market_data', 'get_current_position', 'place_market_order',
            'execute_strategy', 'run'
        ]
        
        for method in required_methods:
            if hasattr(BybitTradingBot, method):
                print(f"✓ Method {method} exists")
            else:
                print(f"✗ Method {method} missing")
                return False
        
        print("✓ Bot class structure is correct")
        return True
    except Exception as e:
        print(f"✗ Bot class error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all debug tests"""
    print("=== Bybit Trading Bot Debug ===")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print()
    
    tests = [
        test_imports,
        test_logger,
        test_config_loading,
        test_strategy,
        test_bot_class,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Unexpected error in {test.__name__}: {e}")
            failed += 1
        print()
    
    print("=== Debug Summary ===")
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")
    
    if failed == 0:
        print("🎉 All tests passed! Bot should work with valid API keys.")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
