#!/usr/bin/env python3
"""
Quick test to verify the bot setup
"""

def main():
    print("=== Bybit Trading Bot Quick Test ===")
    
    # Test 1: Check configuration
    try:
        import json
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("✓ Config loaded successfully")
        print(f"  API Key: {config['api_key'][:10]}...")
        print(f"  Testnet: {config['testnet']}")
    except Exception as e:
        print(f"✗ Config error: {e}")
        return False
    
    # Test 2: Check imports
    try:
        from pybit.unified_trading import HTTP
        print("✓ PyBit imported")
        
        from utils.logger import setup_logger
        print("✓ Logger imported")
        
        from strategies.moving_average import MovingAverageStrategy
        print("✓ Strategy imported")
        
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False
    
    # Test 3: Test API connection
    try:
        client = HTTP(
            api_key=config['api_key'],
            api_secret=config['api_secret'],
            testnet=config['testnet']
        )
        
        # Simple API test
        response = client.get_wallet_balance(accountType="UNIFIED")
        if response['retCode'] == 0:
            print("✓ API connection successful")
        else:
            print(f"✗ API error: {response['retMsg']}")
            return False
            
    except Exception as e:
        print(f"✗ API connection failed: {e}")
        return False
    
    print("\n🎉 All tests passed! Bot is ready to run.")
    print("\nNext steps:")
    print("1. Run: python bot.py")
    print("2. Or press F5 in VS Code to debug")
    
    return True

if __name__ == "__main__":
    main()
