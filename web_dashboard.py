#!/usr/bin/env python3
"""
Web Dashboard for Bybit Trading Bot
Real-time trading dashboard with live updates
"""

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import json
import threading
import time
from datetime import datetime
import logging
from pybit.unified_trading import HTTP
from strategies.moving_average import MovingAverageStrategy
from utils.logger import setup_logger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bybit_trading_bot_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

class TradingBotWebInterface:
    def __init__(self, config_path="config.json"):
        self.logger = setup_logger("WebInterface")
        self.config = self.load_config(config_path)
        self.client = self.initialize_client()
        self.strategy = MovingAverageStrategy(
            short_period=self.config.get("ma_short_period", 20),
            long_period=self.config.get("ma_long_period", 50)
        )
        
        self.bot_start_time = datetime.now()
        self.trade_history = []
        self.current_positions = {}
        self.latest_signals = {}
        self.running = False
        
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
            return config
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return {}
    
    def initialize_client(self):
        """Initialize Bybit client"""
        try:
            if not self.config.get('api_key') or self.config.get('api_key') == 'YOUR_BYBIT_API_KEY_HERE':
                self.logger.warning("API keys not configured - using demo mode")
                return None
                
            client = HTTP(
                api_key=self.config['api_key'],
                api_secret=self.config['api_secret'],
                testnet=self.config.get('testnet', True)
            )
            
            # Test connection with timeout handling
            try:
                response = client.get_wallet_balance(accountType="UNIFIED")
                if response['retCode'] == 0:
                    self.logger.info("Connected to Bybit API")
                    return client
                else:
                    self.logger.error(f"API connection failed: {response['retMsg']}")
                    return None
            except Exception as conn_error:
                self.logger.warning(f"API connection timeout: {conn_error}")
                self.logger.info("Continuing in demo mode")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to initialize client: {e}")
            return None
    
    def get_account_balance(self):
        """Get account balance"""
        if not self.client:
            return 10000.0  # Demo balance
            
        try:
            response = self.client.get_wallet_balance(accountType="UNIFIED", coin="USDT")
            if response['retCode'] == 0 and response['result']['list']:
                balance_data = response['result']['list'][0]['coin'][0]
                return float(balance_data['availableToWithdraw'])
        except Exception as e:
            self.logger.error(f"Error getting balance: {e}")
        
        return 0.0
    
    def get_market_data(self, symbol):
        """Get market data for symbol"""
        if not self.client:
            # Demo data
            import random
            base_price = 50000 if symbol == "BTCUSDT" else 3000
            price = base_price + random.uniform(-1000, 1000)
            return {
                'price': price,
                'ma_short': price + random.uniform(-100, 100),
                'ma_long': price + random.uniform(-200, 200)
            }
            
        try:
            response = self.client.get_kline(
                category="linear",
                symbol=symbol,
                interval="5",
                limit=100
            )
            
            if response['retCode'] == 0:
                current_price = float(response['result']['list'][0][4])
                signal, ma_short, ma_long = self.strategy.get_current_signal(response)
                
                return {
                    'price': current_price,
                    'ma_short': ma_short if ma_short else current_price,
                    'ma_long': ma_long if ma_long else current_price,
                    'signal': signal
                }
        except Exception as e:
            self.logger.error(f"Error getting market data: {e}")
        
        return None
    
    def get_current_positions(self):
        """Get current positions"""
        if not self.client:
            # Demo positions
            return []
            
        try:
            positions = []
            for symbol in self.config.get('trading_pairs', ['BTCUSDT']):
                response = self.client.get_positions(category="linear", symbol=symbol)
                if response['retCode'] == 0 and response['result']['list']:
                    position_data = response['result']['list'][0]
                    if float(position_data['size']) > 0:
                        positions.append({
                            'symbol': position_data['symbol'],
                            'side': position_data['side'],
                            'size': float(position_data['size']),
                            'avg_price': float(position_data['avgPrice']) if position_data['avgPrice'] else 0,
                            'unrealized_pnl': float(position_data['unrealisedPnl']),
                            'percentage': float(position_data['unrealisedPnl']) / float(position_data['positionValue']) * 100 if float(position_data['positionValue']) > 0 else 0
                        })
            return positions
        except Exception as e:
            self.logger.error(f"Error getting positions: {e}")
            return []
    
    def calculate_total_pnl(self):
        """Calculate total P&L"""
        positions = self.get_current_positions()
        return sum(pos['unrealized_pnl'] for pos in positions)
    
    def get_uptime(self):
        """Get bot uptime"""
        uptime = datetime.now() - self.bot_start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def update_loop(self):
        """Main update loop for sending real-time data"""
        while self.running:
            try:
                # Get current data
                balance = self.get_account_balance()
                positions = self.get_current_positions()
                total_pnl = self.calculate_total_pnl()
                uptime = self.get_uptime()
                
                # Emit bot status
                socketio.emit('bot_status', {
                    'balance': balance,
                    'total_pnl': total_pnl,
                    'active_positions': len(positions),
                    'uptime': uptime
                })
                
                # Emit position updates
                socketio.emit('position_update', {
                    'positions': positions
                })
                
                # Update trading signals and prices for each pair
                for symbol in self.config.get('trading_pairs', ['BTCUSDT', 'ETHUSDT']):
                    market_data = self.get_market_data(symbol)
                    if market_data:
                        # Emit trading signal
                        socketio.emit('trading_signal', {
                            'symbol': symbol,
                            'signal': market_data.get('signal'),
                            'price': market_data['price'],
                            'ma_short': market_data['ma_short'],
                            'ma_long': market_data['ma_long']
                        })
                        
                        # Emit price update for charts
                        socketio.emit('price_update', {
                            'symbol': symbol,
                            'price': market_data['price'],
                            'ma_short': market_data['ma_short'],
                            'ma_long': market_data['ma_long']
                        })
                
                # Emit trade history
                socketio.emit('trade_history', {
                    'trades': self.trade_history[-10:]  # Last 10 trades
                })
                
                time.sleep(5)  # Update every 5 seconds
                
            except Exception as e:
                self.logger.error(f"Error in update loop: {e}")
                time.sleep(10)
    
    def start_monitoring(self):
        """Start the monitoring thread"""
        self.running = True
        self.monitor_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Web interface monitoring started")
    
    def stop_monitoring(self):
        """Stop the monitoring thread"""
        self.running = False
        self.logger.info("Web interface monitoring stopped")

# Global bot interface instance
bot_interface = TradingBotWebInterface()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    """API endpoint for bot status"""
    return jsonify({
        'status': 'running' if bot_interface.running else 'stopped',
        'balance': bot_interface.get_account_balance(),
        'total_pnl': bot_interface.calculate_total_pnl(),
        'active_positions': len(bot_interface.get_current_positions()),
        'uptime': bot_interface.get_uptime()
    })

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('status', {'msg': 'Connected to trading bot dashboard'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

@socketio.on('request_initial_data')
def handle_initial_data():
    """Send initial data when client requests it"""
    # Send current status
    balance = bot_interface.get_account_balance()
    positions = bot_interface.get_current_positions()
    total_pnl = bot_interface.calculate_total_pnl()
    uptime = bot_interface.get_uptime()
    
    emit('bot_status', {
        'balance': balance,
        'total_pnl': total_pnl,
        'active_positions': len(positions),
        'uptime': uptime
    })
    
    emit('position_update', {
        'positions': positions
    })

if __name__ == '__main__':
    try:
        print("Starting Bybit Trading Bot Web Dashboard...")
        print("Dashboard will be available at: http://localhost:5000")
        print("Press Ctrl+C to stop")
        
        # Start monitoring
        bot_interface.start_monitoring()
        
        # Run Flask app
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
        
    except KeyboardInterrupt:
        print("\nStopping dashboard...")
        bot_interface.stop_monitoring()
    except Exception as e:
        print(f"Error starting dashboard: {e}")
        logging.exception("Dashboard startup error")
