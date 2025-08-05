#!/usr/bin/env python3
"""
Comprehensive debug script for Bybit Trading Bot
Tests all components and identifies issues
"""

import sys
import traceback
import importlib
import json
import os
from datetime import datetime

def test_python_environment():
    """Test Python environment and version"""
    print("🐍 Testing Python Environment...")
    print(f"   Python Version: {sys.version}")
    print(f"   Python Executable: {sys.executable}")
    print(f"   Current Directory: {os.getcwd()}")
    print("   ✅ Python environment OK\n")

def test_required_imports():
    """Test all required imports"""
    print("📦 Testing Required Imports...")
    
    required_packages = [
        ('json', 'Standard Library'),
        ('time', 'Standard Library'),
        ('os', 'Standard Library'),
        ('datetime', 'Standard Library'),
        ('logging', 'Standard Library'),
        ('threading', 'Standard Library'),
        ('pandas', 'Data Analysis'),
        ('numpy', 'Numerical Computing'),
        ('requests', 'HTTP Library'),
        ('pybit.unified_trading', 'Bybit API'),
        ('flask', 'Web Framework'),
        ('flask_socketio', 'WebSocket Support'),
    ]
    
    failed_imports = []
    
    for package, description in required_packages:
        try:
            if '.' in package:
                module_name, class_name = package.rsplit('.', 1)
                module = importlib.import_module(module_name)
                getattr(module, class_name)
            else:
                importlib.import_module(package)
            print(f"   ✅ {package} ({description})")
        except ImportError as e:
            print(f"   ❌ {package} ({description}) - {e}")
            failed_imports.append(package)
        except Exception as e:
            print(f"   ⚠️  {package} ({description}) - {e}")
    
    if failed_imports:
        print(f"\n❌ Failed imports: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ All imports successful\n")
        return True

def test_config_file():
    """Test configuration file"""
    print("⚙️ Testing Configuration...")
    
    try:
        if not os.path.exists('config.json'):
            print("   ❌ config.json not found")
            if os.path.exists('config.example.json'):
                print("   💡 Found config.example.json - copy it to config.json")
            return False
        
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # Check required fields
        required_fields = ['api_key', 'api_secret', 'testnet', 'trading_pairs']
        missing_fields = []
        
        for field in required_fields:
            if field not in config:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"   ❌ Missing fields: {', '.join(missing_fields)}")
            return False
        
        # Check if API keys are set
        if config['api_key'] == 'YOUR_BYBIT_API_KEY_HERE':
            print("   ⚠️  API key still has placeholder value")
        else:
            print(f"   ✅ API Key configured: {config['api_key'][:10]}...")
        
        if config['api_secret'] == 'YOUR_BYBIT_API_SECRET_HERE':
            print("   ⚠️  API secret still has placeholder value")
        else:
            print("   ✅ API Secret configured")
        
        print(f"   ✅ Testnet Mode: {config['testnet']}")
        print(f"   ✅ Trading Pairs: {config['trading_pairs']}")
        print("   ✅ Configuration file OK\n")
        return True
        
    except json.JSONDecodeError as e:
        print(f"   ❌ Invalid JSON in config.json: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Config error: {e}")
        return False

def test_local_modules():
    """Test local modules"""
    print("🔧 Testing Local Modules...")
    
    modules_to_test = [
        ('utils.logger', 'setup_logger'),
        ('strategies.moving_average', 'MovingAverageStrategy'),
    ]
    
    for module_path, class_name in modules_to_test:
        try:
            module = importlib.import_module(module_path)
            if hasattr(module, class_name):
                print(f"   ✅ {module_path}.{class_name}")
            else:
                print(f"   ❌ {module_path}.{class_name} not found")
                return False
        except ImportError as e:
            print(f"   ❌ {module_path} import failed: {e}")
            return False
        except Exception as e:
            print(f"   ❌ {module_path} error: {e}")
            return False
    
    print("   ✅ All local modules OK\n")
    return True

def test_bot_class():
    """Test main bot class"""
    print("🤖 Testing Bot Class...")
    
    try:
        from bot import BybitTradingBot
        
        # Test class instantiation (might fail if API keys are invalid)
        try:
            bot = BybitTradingBot()
            print("   ✅ Bot class instantiated successfully")
            
            # Test method existence
            required_methods = [
                'load_config', 'initialize_client', 'get_account_balance',
                'get_market_data', 'execute_strategy', 'run'
            ]
            
            for method in required_methods:
                if hasattr(bot, method):
                    print(f"   ✅ Method {method} exists")
                else:
                    print(f"   ❌ Method {method} missing")
                    return False
            
        except Exception as e:
            print(f"   ⚠️  Bot instantiation failed: {e}")
            print("   💡 This might be due to API configuration issues")
        
        print("   ✅ Bot class structure OK\n")
        return True
        
    except ImportError as e:
        print(f"   ❌ Bot import failed: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Bot class error: {e}")
        return False

def test_web_dashboard():
    """Test web dashboard components"""
    print("🌐 Testing Web Dashboard...")
    
    try:
        # Test web dashboard import
        import web_dashboard
        print("   ✅ Web dashboard module imported")
        
        # Test Flask app creation
        app = web_dashboard.app
        print("   ✅ Flask app created")
        
        # Test bot interface
        bot_interface = web_dashboard.bot_interface
        print("   ✅ Bot interface created")
        
        # Test template file
        if os.path.exists('templates/dashboard.html'):
            print("   ✅ Dashboard template exists")
        else:
            print("   ❌ Dashboard template missing")
            return False
        
        print("   ✅ Web dashboard OK\n")
        return True
        
    except ImportError as e:
        print(f"   ❌ Web dashboard import failed: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Web dashboard error: {e}")
        return False

def test_api_connection():
    """Test API connection"""
    print("🔗 Testing API Connection...")
    
    try:
        from pybit.unified_trading import HTTP
        
        # Load config
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        if config['api_key'] == 'YOUR_BYBIT_API_KEY_HERE':
            print("   ⚠️  API keys not configured - skipping connection test")
            print("   💡 Update config.json with real API keys to test connection")
            return True
        
        # Test connection
        client = HTTP(
            api_key=config['api_key'],
            api_secret=config['api_secret'],
            testnet=config.get('testnet', True)
        )
        
        response = client.get_wallet_balance(accountType="UNIFIED")
        
        if response['retCode'] == 0:
            print("   ✅ API connection successful")
            
            # Get balance info
            if response['result']['list']:
                wallet = response['result']['list'][0]
                print(f"   ✅ Account Type: {wallet['accountType']}")
                
                if wallet['coin']:
                    for coin_data in wallet['coin']:
                        coin = coin_data['coin']
                        balance = float(coin_data['walletBalance'])
                        if balance > 0:
                            print(f"   💰 {coin}: {balance:.6f}")
                else:
                    print("   ℹ️  No coin balances (normal for new testnet accounts)")
            
        else:
            print(f"   ❌ API connection failed: {response['retMsg']}")
            return False
        
        print("   ✅ API connection OK\n")
        return True
        
    except Exception as e:
        print(f"   ❌ API connection error: {e}")
        traceback.print_exc()
        return False

def test_strategy():
    """Test trading strategy"""
    print("📈 Testing Trading Strategy...")
    
    try:
        from strategies.moving_average import MovingAverageStrategy
        import numpy as np
        
        # Create strategy instance
        strategy = MovingAverageStrategy(short_period=5, long_period=10)
        print("   ✅ Strategy instance created")
        
        # Create sample data
        sample_data = {
            'result': {
                'list': []
            }
        }
        
        # Generate sample klines
        base_price = 50000
        for i in range(20):
            timestamp = int(datetime.now().timestamp() * 1000) - (19-i) * 60000
            price = base_price + np.random.normal(0, 100)
            sample_data['result']['list'].append([
                str(timestamp),
                str(price - 50),    # open
                str(price + 100),   # high
                str(price - 100),   # low
                str(price),         # close
                str(1000)           # volume
            ])
        
        # Test strategy
        signal, ma_short, ma_long = strategy.get_current_signal(sample_data)
        
        print(f"   ✅ Strategy signal: {signal or 'HOLD'}")
        print(f"   ✅ MA Short: {ma_short:.2f}" if ma_short else "   ✅ MA Short: None")
        print(f"   ✅ MA Long: {ma_long:.2f}" if ma_long else "   ✅ MA Long: None")
        
        print("   ✅ Trading strategy OK\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Strategy error: {e}")
        traceback.print_exc()
        return False

def test_file_structure():
    """Test file structure"""
    print("📁 Testing File Structure...")
    
    required_files = [
        'bot.py',
        'web_dashboard.py',
        'start_dashboard.py',
        'requirements.txt',
        'web_requirements.txt',
        'config.example.json',
        'utils/__init__.py',
        'utils/logger.py',
        'strategies/__init__.py',
        'strategies/moving_average.py',
        'templates/dashboard.html'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("   ✅ All required files present\n")
        return True

def test_dependencies():
    """Test if all dependencies are installed"""
    print("📋 Testing Dependencies...")
    
    # Test core dependencies
    try:
        with open('requirements.txt', 'r') as f:
            core_deps = f.read().strip().split('\n')
        
        for dep in core_deps:
            if dep.strip():
                package_name = dep.split('==')[0].split('>=')[0].split('<=')[0]
                try:
                    importlib.import_module(package_name.replace('-', '_'))
                    print(f"   ✅ {package_name}")
                except ImportError:
                    print(f"   ❌ {package_name} not installed")
    
    except FileNotFoundError:
        print("   ❌ requirements.txt not found")
    
    # Test web dependencies
    try:
        with open('web_requirements.txt', 'r') as f:
            web_deps = f.read().strip().split('\n')
        
        for dep in web_deps:
            if dep.strip():
                package_name = dep.split('==')[0].split('>=')[0].split('<=')[0]
                try:
                    importlib.import_module(package_name.replace('-', '_'))
                    print(f"   ✅ {package_name}")
                except ImportError:
                    print(f"   ❌ {package_name} not installed")
    
    except FileNotFoundError:
        print("   ❌ web_requirements.txt not found")
    
    print("   ✅ Dependencies check complete\n")
    return True

def generate_fix_recommendations(failed_tests):
    """Generate fix recommendations based on failed tests"""
    print("🔧 Fix Recommendations:")
    print("=" * 50)
    
    if not failed_tests:
        print("🎉 All tests passed! Your trading bot is ready to use.")
        print("\nTo start trading:")
        print("1. Web Dashboard: python start_dashboard.py")
        print("2. Command Line: python bot.py")
        return
    
    for test_name in failed_tests:
        print(f"\n❌ {test_name} failed:")
        
        if test_name == "Required Imports":
            print("   Fix: pip install -r requirements.txt")
            print("   Fix: pip install -r web_requirements.txt")
        
        elif test_name == "Configuration":
            print("   Fix: copy config.example.json config.json")
            print("   Fix: Edit config.json with your Bybit API keys")
        
        elif test_name == "Local Modules":
            print("   Fix: Check file structure and imports")
            print("   Fix: Ensure all Python files have correct syntax")
        
        elif test_name == "Bot Class":
            print("   Fix: Check bot.py for syntax errors")
            print("   Fix: Verify API configuration in config.json")
        
        elif test_name == "Web Dashboard":
            print("   Fix: pip install flask flask-socketio")
            print("   Fix: Check templates/dashboard.html exists")
        
        elif test_name == "API Connection":
            print("   Fix: Verify API keys in config.json")
            print("   Fix: Check internet connection")
            print("   Fix: Ensure testnet=true for testing")
        
        elif test_name == "Trading Strategy":
            print("   Fix: Check strategies/moving_average.py")
            print("   Fix: pip install pandas numpy")
        
        elif test_name == "File Structure":
            print("   Fix: Recreate missing files")
            print("   Fix: Check git repository integrity")

def main():
    """Run all debug tests"""
    print("🔍 BYBIT TRADING BOT - COMPREHENSIVE DEBUG")
    print("=" * 60)
    print(f"📅 Debug Time: {datetime.now()}")
    print(f"📂 Working Directory: {os.getcwd()}")
    print("=" * 60)
    
    tests = [
        ("Python Environment", test_python_environment),
        ("Required Imports", test_required_imports),
        ("File Structure", test_file_structure),
        ("Configuration", test_config_file),
        ("Dependencies", test_dependencies),
        ("Local Modules", test_local_modules),
        ("Trading Strategy", test_strategy),
        ("Bot Class", test_bot_class),
        ("Web Dashboard", test_web_dashboard),
        ("API Connection", test_api_connection),
    ]
    
    passed_tests = []
    failed_tests = []
    
    for test_name, test_func in tests:
        try:
            print(f"Running {test_name}...")
            if test_func():
                passed_tests.append(test_name)
            else:
                failed_tests.append(test_name)
        except Exception as e:
            print(f"   ❌ Unexpected error in {test_name}: {e}")
            failed_tests.append(test_name)
    
    # Summary
    print("=" * 60)
    print("📊 DEBUG SUMMARY")
    print("=" * 60)
    print(f"✅ Tests Passed: {len(passed_tests)}")
    print(f"❌ Tests Failed: {len(failed_tests)}")
    print(f"📈 Success Rate: {len(passed_tests)/(len(tests))*100:.1f}%")
    
    if passed_tests:
        print(f"\n✅ Passed: {', '.join(passed_tests)}")
    
    if failed_tests:
        print(f"\n❌ Failed: {', '.join(failed_tests)}")
    
    print("\n" + "=" * 60)
    generate_fix_recommendations(failed_tests)
    
    return len(failed_tests) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
