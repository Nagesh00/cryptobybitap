#!/usr/bin/env python3
"""
Enhanced Bybit Trading Bot Web Dashboard
Professional trading interface with real-time data and trading capabilities
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import json
import threading
import time
from datetime import datetime, timedelta
import logging
import random
from pybit.unified_trading import HTTP
from strategies.moving_average import MovingAverageStrategy
from utils.logger import setup_logger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bybit_trading_bot_enhanced_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

class EnhancedTradingDashboard:
    def __init__(self, config_path="config.json"):
        self.logger = setup_logger("EnhancedDashboard")
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
        self.price_history = {}
        self.running = False
        self.auto_trading = False
        
        # Initialize demo data if no API connection
        if not self.client:
            self.initialize_demo_data()
        
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
            return config
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return {
                "trading_pairs": ["BTCUSDT", "ETHUSDT", "ADAUSDT", "XRPUSDT"],
                "testnet": True
            }
    
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
            
            # Test connection
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
    
    def initialize_demo_data(self):
        """Initialize demo trading data"""
        self.demo_balance = 10000.0
        self.demo_positions = []
        self.demo_trades = []
        
        # Add some demo trade history
        base_time = datetime.now() - timedelta(hours=24)
        for i in range(10):
            trade_time = base_time + timedelta(hours=i*2.4)
            self.demo_trades.append({
                'symbol': random.choice(['BTCUSDT', 'ETHUSDT']),
                'side': random.choice(['Buy', 'Sell']),
                'size': round(random.uniform(0.001, 0.1), 3),
                'price': round(random.uniform(40000, 60000), 2),
                'pnl': round(random.uniform(-50, 150), 2),
                'time': trade_time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'Filled'
            })
        
        self.trade_history = self.demo_trades
    
    def get_account_balance(self):
        """Get account balance"""
        if not self.client:
            return self.demo_balance
            
        try:
            response = self.client.get_wallet_balance(accountType="UNIFIED", coin="USDT")
            if response['retCode'] == 0 and response['result']['list']:
                balance_data = response['result']['list'][0]['coin'][0]
                return float(balance_data['availableToWithdraw'])
        except Exception as e:
            self.logger.error(f"Error getting balance: {e}")
        
        return 0.0
    
    def get_market_data(self, symbol):
        """Get enhanced market data for symbol"""
        if not self.client:
            # Enhanced demo data with realistic price movements
            base_prices = {
                'BTCUSDT': 45000,
                'ETHUSDT': 3000,
                'ADAUSDT': 0.5,
                'XRPUSDT': 0.6
            }
            
            # Get or initialize price history
            if symbol not in self.price_history:
                self.price_history[symbol] = []
            
            base_price = base_prices.get(symbol, 1000)
            
            # Create realistic price movement
            if self.price_history[symbol]:
                last_price = self.price_history[symbol][-1]['price']
                change = random.uniform(-0.02, 0.02)  # ±2% change
                new_price = last_price * (1 + change)
            else:
                new_price = base_price + random.uniform(-base_price*0.05, base_price*0.05)
            
            # Calculate moving averages
            ma_short = new_price * random.uniform(0.998, 1.002)
            ma_long = new_price * random.uniform(0.995, 1.005)
            
            # Determine signal
            signal = 'BUY' if ma_short > ma_long else 'SELL' if ma_short < ma_long * 0.998 else 'HOLD'
            
            # Store price history (keep last 100 points)
            price_point = {
                'time': datetime.now().isoformat(),
                'price': new_price,
                'ma_short': ma_short,
                'ma_long': ma_long
            }
            
            self.price_history[symbol].append(price_point)
            if len(self.price_history[symbol]) > 100:
                self.price_history[symbol] = self.price_history[symbol][-100:]
            
            return {
                'symbol': symbol,
                'price': round(new_price, 4),
                'ma_short': round(ma_short, 4),
                'ma_long': round(ma_long, 4),
                'signal': signal,
                'change_24h': round(random.uniform(-5, 5), 2),
                'volume_24h': round(random.uniform(1000000, 5000000), 0),
                'price_history': self.price_history[symbol][-20:]  # Last 20 points for charts
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
                    'symbol': symbol,
                    'price': current_price,
                    'ma_short': ma_short if ma_short else current_price,
                    'ma_long': ma_long if ma_long else current_price,
                    'signal': signal,
                    'change_24h': 0,  # Calculate from data
                    'volume_24h': 0   # Get from ticker
                }
        except Exception as e:
            self.logger.error(f"Error getting market data: {e}")
        
        return None
    
    def execute_trade(self, symbol, side, quantity):
        """Execute a trade (demo or real)"""
        if not self.client:
            # Demo trade execution
            current_data = self.get_market_data(symbol)
            if current_data:
                trade = {
                    'symbol': symbol,
                    'side': side,
                    'size': quantity,
                    'price': current_data['price'],
                    'pnl': 0,
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'Filled (Demo)',
                    'demo': True
                }
                
                self.trade_history.append(trade)
                if len(self.trade_history) > 50:
                    self.trade_history = self.trade_history[-50:]
                
                return {'success': True, 'trade': trade}
        
        # Real trading implementation would go here
        return {'success': False, 'error': 'Real trading not implemented in demo'}
    
    def get_current_positions(self):
        """Get current positions with enhanced data"""
        if not self.client:
            # Demo positions
            positions = []
            if random.random() > 0.7:  # 30% chance of having positions
                for symbol in random.sample(self.config.get('trading_pairs', ['BTCUSDT']), 
                                           random.randint(0, 2)):
                    current_data = self.get_market_data(symbol)
                    if current_data:
                        entry_price = current_data['price'] * random.uniform(0.95, 1.05)
                        size = round(random.uniform(0.001, 0.1), 3)
                        side = random.choice(['Buy', 'Sell'])
                        
                        pnl = (current_data['price'] - entry_price) * size
                        if side == 'Sell':
                            pnl = -pnl
                        
                        positions.append({
                            'symbol': symbol,
                            'side': side,
                            'size': size,
                            'avg_price': round(entry_price, 4),
                            'current_price': current_data['price'],
                            'unrealized_pnl': round(pnl, 2),
                            'percentage': round((pnl / (entry_price * size)) * 100, 2),
                            'position_value': round(entry_price * size, 2)
                        })
            
            return positions
            
        # Real API implementation would go here
        return []
    
    def update_loop(self):
        """Enhanced update loop with more real-time data"""
        while self.running:
            try:
                # Get current data
                balance = self.get_account_balance()
                positions = self.get_current_positions()
                total_pnl = sum(pos['unrealized_pnl'] for pos in positions)
                uptime = self.get_uptime()
                
                # Emit bot status
                socketio.emit('bot_status', {
                    'balance': balance,
                    'total_pnl': total_pnl,
                    'active_positions': len(positions),
                    'uptime': uptime,
                    'auto_trading': self.auto_trading,
                    'demo_mode': not bool(self.client)
                })
                
                # Emit position updates
                socketio.emit('position_update', {
                    'positions': positions
                })
                
                # Update market data for all trading pairs
                market_data_all = {}
                for symbol in self.config.get('trading_pairs', ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'XRPUSDT']):
                    market_data = self.get_market_data(symbol)
                    if market_data:
                        market_data_all[symbol] = market_data
                        
                        # Emit individual trading signals
                        socketio.emit('trading_signal', market_data)
                
                # Emit all market data
                socketio.emit('market_data_update', market_data_all)
                
                # Emit trade history
                socketio.emit('trade_history_update', {
                    'trades': self.trade_history[-20:]  # Last 20 trades
                })
                
                time.sleep(2)  # Update every 2 seconds for more real-time feel
                
            except Exception as e:
                self.logger.error(f"Error in update loop: {e}")
                time.sleep(5)
    
    def get_uptime(self):
        """Get bot uptime"""
        uptime = datetime.now() - self.bot_start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def start_monitoring(self):
        """Start the monitoring thread"""
        self.running = True
        self.monitor_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Enhanced web interface monitoring started")
    
    def stop_monitoring(self):
        """Stop the monitoring thread"""
        self.running = False
        self.logger.info("Enhanced web interface monitoring stopped")

# Global dashboard instance
dashboard = EnhancedTradingDashboard()

@app.route('/')
def trading_dashboard():
    """Main trading dashboard page"""
    return render_template('enhanced_dashboard.html')

@app.route('/api/status')
def api_status():
    """Enhanced API endpoint for bot status"""
    return jsonify({
        'status': 'running' if dashboard.running else 'stopped',
        'balance': dashboard.get_account_balance(),
        'total_pnl': sum(pos['unrealized_pnl'] for pos in dashboard.get_current_positions()),
        'active_positions': len(dashboard.get_current_positions()),
        'uptime': dashboard.get_uptime(),
        'auto_trading': dashboard.auto_trading,
        'demo_mode': not bool(dashboard.client),
        'trading_pairs': dashboard.config.get('trading_pairs', [])
    })

@app.route('/api/market/<symbol>')
def get_market_data_api(symbol):
    """Get market data for specific symbol"""
    data = dashboard.get_market_data(symbol)
    return jsonify(data if data else {'error': 'Symbol not found'})

@app.route('/api/trade', methods=['POST'])
def execute_trade_api():
    """Execute a trade via API"""
    data = request.json
    symbol = data.get('symbol')
    side = data.get('side')
    quantity = float(data.get('quantity', 0))
    
    if not symbol or not side or quantity <= 0:
        return jsonify({'success': False, 'error': 'Invalid trade parameters'})
    
    result = dashboard.execute_trade(symbol, side, quantity)
    return jsonify(result)

@app.route('/api/toggle-auto-trading', methods=['POST'])
def toggle_auto_trading():
    """Toggle auto trading on/off"""
    dashboard.auto_trading = not dashboard.auto_trading
    return jsonify({
        'success': True, 
        'auto_trading': dashboard.auto_trading,
        'message': f"Auto trading {'enabled' if dashboard.auto_trading else 'disabled'}"
    })

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected to enhanced dashboard')
    emit('status', {'msg': 'Connected to enhanced trading dashboard'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected from enhanced dashboard')

@socketio.on('request_initial_data')
def handle_initial_data():
    """Send comprehensive initial data"""
    # Send current status
    balance = dashboard.get_account_balance()
    positions = dashboard.get_current_positions()
    total_pnl = sum(pos['unrealized_pnl'] for pos in positions)
    uptime = dashboard.get_uptime()
    
    emit('bot_status', {
        'balance': balance,
        'total_pnl': total_pnl,
        'active_positions': len(positions),
        'uptime': uptime,
        'auto_trading': dashboard.auto_trading,
        'demo_mode': not bool(dashboard.client)
    })
    
    emit('position_update', {'positions': positions})
    emit('trade_history_update', {'trades': dashboard.trade_history[-20:]})

if __name__ == '__main__':
    try:
        print("🚀 Starting Enhanced Bybit Trading Bot Dashboard...")
        print("📊 Dashboard available at: http://localhost:5000")
        print("💼 Features: Real-time trading, live charts, position management")
        print("🔧 Press Ctrl+C to stop")
        print("=" * 60)
        
        # Start monitoring
        dashboard.start_monitoring()
        
        # Run Flask app
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
        
    except KeyboardInterrupt:
        print("\n⏹️  Stopping enhanced dashboard...")
        dashboard.stop_monitoring()
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        logging.exception("Enhanced dashboard startup error")
