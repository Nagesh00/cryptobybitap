#!/usr/bin/env python3
"""
Test Bybit API connection with the provided credentials
"""

import json
import sys
from pybit.unified_trading import HTTP

def test_api_connection():
    """Test connection to Bybit API"""
    try:
        # Load configuration
        with open('config.json', 'r') as file:
            config = json.load(file)
        
        print("Testing Bybit API connection...")
        print(f"API Key: {config['api_key'][:10]}...")
        print(f"Using Testnet: {config['testnet']}")
        
        # Initialize client
        client = HTTP(
            api_key=config['api_key'],
            api_secret=config['api_secret'],
            testnet=config.get('testnet', True)
        )
        
        # Test connection by getting wallet balance
        print("\nTesting wallet balance retrieval...")
        response = client.get_wallet_balance(accountType="UNIFIED")
        
        if response['retCode'] == 0:
            print("✓ API connection successful!")
            
            # Display wallet information
            if response['result']['list']:
                wallet = response['result']['list'][0]
                print(f"Account Type: {wallet['accountType']}")
                
                if wallet['coin']:
                    print("\nWallet Balances:")
                    for coin_data in wallet['coin']:
                        coin = coin_data['coin']
                        balance = float(coin_data['walletBalance'])
                        available = float(coin_data['availableToWithdraw'])
                        
                        if balance > 0:
                            print(f"  {coin}: {balance:.6f} (Available: {available:.6f})")
                else:
                    print("No coin balances found (this is normal for new testnet accounts)")
            else:
                print("No wallet data found")
                
        else:
            print(f"✗ API connection failed: {response['retMsg']}")
            return False
            
        # Test getting market data
        print("\nTesting market data retrieval...")
        market_response = client.get_kline(
            category="linear",
            symbol="BTCUSDT",
            interval="5",
            limit=5
        )
        
        if market_response['retCode'] == 0:
            print("✓ Market data retrieval successful!")
            
            if market_response['result']['list']:
                latest_kline = market_response['result']['list'][0]
                current_price = float(latest_kline[4])  # Close price
                print(f"Current BTCUSDT price: ${current_price:,.2f}")
            
        else:
            print(f"✗ Market data failed: {market_response['retMsg']}")
            return False
            
        print("\n🎉 All API tests passed! Your bot should work correctly.")
        return True
        
    except Exception as e:
        print(f"✗ Error testing API: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api_connection()
    if not success:
        print("\n❌ API test failed. Please check your credentials.")
        sys.exit(1)
    else:
        print("\n✅ Ready to run the trading bot!")
        sys.exit(0)
