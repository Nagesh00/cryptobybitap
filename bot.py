import json
import time
import os
from datetime import datetime
from pybit.unified_trading import HTTP
from strategies.moving_average import MovingAverageStrategy
from utils.logger import setup_logger

class BybitTradingBot:
    def __init__(self, config_path="config.json"):
        self.logger = setup_logger("BybitTradingBot")
        self.config = self.load_config(config_path)
        self.client = self.initialize_client()
        self.strategy = MovingAverageStrategy(
            short_period=self.config.get("ma_short_period", 20),
            long_period=self.config.get("ma_long_period", 50)
        )
        self.positions = {}
        
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
            
            # Validate required fields
            required_fields = ['api_key', 'api_secret']
            for field in required_fields:
                if field not in config or not config[field] or config[field] == f"YOUR_BYBIT_{field.upper()}_HERE":
                    raise ValueError(f"Please set your {field} in {config_path}")
            
            self.logger.info("Configuration loaded successfully")
            return config
            
        except FileNotFoundError:
            self.logger.error(f"Configuration file {config_path} not found")
            raise
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON in {config_path}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            raise
    
    def initialize_client(self):
        """Initialize Bybit client"""
        try:
            client = HTTP(
                api_key=self.config['api_key'],
                api_secret=self.config['api_secret'],
                testnet=self.config.get('testnet', True)
            )
            
            # Test connection
            balance = client.get_wallet_balance(accountType="UNIFIED")
            self.logger.info(f"Connected to Bybit {'Testnet' if self.config.get('testnet') else 'Mainnet'}")
            
            return client
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Bybit client: {e}")
            raise
    
    def get_account_balance(self, coin="USDT"):
        """Get account balance for specific coin"""
        try:
            response = self.client.get_wallet_balance(
                accountType="UNIFIED",
                coin=coin
            )
            
            if response['retCode'] == 0:
                balance_data = response['result']['list'][0]['coin'][0]
                available_balance = float(balance_data['availableToWithdraw'])
                return available_balance
            else:
                self.logger.error(f"Error getting balance: {response['retMsg']}")
                return 0
                
        except Exception as e:
            self.logger.error(f"Error getting account balance: {e}")
            return 0
    
    def get_market_data(self, symbol, interval="5", limit=200):
        """Get historical market data"""
        try:
            response = self.client.get_kline(
                category="linear",
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            
            if response['retCode'] == 0:
                return response
            else:
                self.logger.error(f"Error getting market data: {response['retMsg']}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting market data: {e}")
            return None
    
    def get_current_position(self, symbol):
        """Get current position for symbol"""
        try:
            response = self.client.get_positions(
                category="linear",
                symbol=symbol
            )
            
            if response['retCode'] == 0 and response['result']['list']:
                position_data = response['result']['list'][0]
                return {
                    'symbol': position_data['symbol'],
                    'side': position_data['side'],
                    'size': float(position_data['size']),
                    'avg_price': float(position_data['avgPrice']) if position_data['avgPrice'] else 0,
                    'unrealized_pnl': float(position_data['unrealisedPnl']),
                    'percentage': float(position_data['unrealisedPnl']) / float(position_data['positionValue']) * 100 if float(position_data['positionValue']) > 0 else 0
                }
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting position: {e}")
            return None
    
    def place_market_order(self, symbol, side, qty, reduce_only=False):
        """Place market order"""
        try:
            order_params = {
                "category": "linear",
                "symbol": symbol,
                "side": side,
                "orderType": "Market",
                "qty": str(qty),
                "timeInForce": "IOC"
            }
            
            if reduce_only:
                order_params["reduceOnly"] = True
            
            response = self.client.place_order(**order_params)
            
            if response['retCode'] == 0:
                self.logger.info(f"Order placed successfully: {side} {qty} {symbol}")
                return response['result']
            else:
                self.logger.error(f"Order failed: {response['retMsg']}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error placing order: {e}")
            return None
    
    def set_stop_loss_take_profit(self, symbol, stop_loss=None, take_profit=None):
        """Set stop loss and take profit for existing position"""
        try:
            params = {
                "category": "linear",
                "symbol": symbol
            }
            
            if stop_loss:
                params["stopLoss"] = str(stop_loss)
            if take_profit:
                params["takeProfit"] = str(take_profit)
            
            response = self.client.set_trading_stop(**params)
            
            if response['retCode'] == 0:
                self.logger.info(f"TP/SL set for {symbol}: SL={stop_loss}, TP={take_profit}")
                return True
            else:
                self.logger.error(f"Failed to set TP/SL: {response['retMsg']}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error setting TP/SL: {e}")
            return False
    
    def calculate_position_size(self, symbol, current_price):
        """Calculate position size based on account balance"""
        try:
            balance = self.get_account_balance()
            max_position_value = balance * 0.1  # Use max 10% of balance
            
            position_size = max_position_value / current_price
            
            # Round to appropriate decimal places
            if symbol.endswith("USDT"):
                if "BTC" in symbol:
                    position_size = round(position_size, 6)
                else:
                    position_size = round(position_size, 4)
            
            return max(position_size, 0.001)  # Minimum position size
            
        except Exception as e:
            self.logger.error(f"Error calculating position size: {e}")
            return self.config.get("position_size", 0.001)
    
    def execute_strategy(self, symbol):
        """Execute trading strategy for a symbol"""
        try:
            # Get market data
            market_data = self.get_market_data(symbol, interval="5", limit=100)
            if not market_data:
                return
            
            # Get current price
            current_price = float(market_data['result']['list'][0][4])
            
            # Get strategy signal
            signal, ma_short, ma_long = self.strategy.get_current_signal(market_data)
            
            # Get current position
            current_position = self.get_current_position(symbol)
            
            self.logger.info(f"{symbol} - Price: {current_price:.4f}, MA Short: {ma_short:.4f}, MA Long: {ma_long:.4f}")
            
            if signal:
                self.logger.info(f"Signal detected for {symbol}: {signal}")
                
                if signal == "BUY" and (not current_position or current_position['size'] == 0):
                    # Open long position
                    position_size = self.calculate_position_size(symbol, current_price)
                    
                    order = self.place_market_order(symbol, "Buy", position_size)
                    if order:
                        # Set stop loss and take profit
                        stop_loss = current_price * (1 - self.config.get("stop_loss_percentage", 2.0) / 100)
                        take_profit = current_price * (1 + self.config.get("take_profit_percentage", 4.0) / 100)
                        
                        time.sleep(1)  # Wait for position to be established
                        self.set_stop_loss_take_profit(symbol, stop_loss, take_profit)
                        
                elif signal == "SELL" and current_position and current_position['size'] > 0:
                    # Close long position
                    self.place_market_order(symbol, "Sell", current_position['size'], reduce_only=True)
            
            # Log current position status
            if current_position and current_position['size'] > 0:
                self.logger.info(f"{symbol} Position: {current_position['side']} {current_position['size']}, "
                               f"PnL: {current_position['unrealized_pnl']:.4f} ({current_position['percentage']:.2f}%)")
                
        except Exception as e:
            self.logger.error(f"Error executing strategy for {symbol}: {e}")
    
    def run(self):
        """Main bot loop"""
        self.logger.info("Starting Bybit Trading Bot")
        self.logger.info(f"Trading pairs: {self.config.get('trading_pairs', [])}")
        self.logger.info(f"Strategy: Moving Average ({self.config.get('ma_short_period', 20)}/{self.config.get('ma_long_period', 50)})")
        
        try:
            while True:
                self.logger.info(f"--- Bot Cycle: {datetime.now()} ---")
                
                # Check account balance
                balance = self.get_account_balance()
                self.logger.info(f"Account Balance: {balance:.4f} USDT")
                
                # Execute strategy for each trading pair
                for symbol in self.config.get('trading_pairs', ['BTCUSDT']):
                    self.execute_strategy(symbol)
                
                # Wait for next cycle
                interval = self.config.get('trading_interval', 60)
                self.logger.info(f"Waiting {interval} seconds for next cycle...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.logger.info("Bot stopped by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
        finally:
            self.logger.info("Bot shut down")

if __name__ == "__main__":
    try:
        bot = BybitTradingBot()
        bot.run()
    except Exception as e:
        print(f"Failed to start bot: {e}")
