# Bybit Trading Bot

A complete cryptocurrency trading bot for Bybit exchange with moving average strategy, risk management, and comprehensive logging.

## Features

- ✅ **Complete Trading Bot** with moving average strategy
- ✅ **Risk Management** with stop loss and take profit
- ✅ **Logging System** with file and console output
- ✅ **Position Management** and tracking
- ✅ **Error Handling** and recovery
- ✅ **Testnet Support** for safe testing
- ✅ **Configurable Parameters** via JSON
- ✅ **Multiple Trading Pairs** support

## Project Structure

```
bybit-trading-bot/
├── bot.py                    # Main bot file
├── web_dashboard.py          # Web dashboard server
├── start_dashboard.py        # Dashboard launcher
├── config.json              # Configuration file
├── requirements.txt         # Python dependencies
├── web_requirements.txt     # Web dashboard dependencies
├── templates/
│   └── dashboard.html       # Web dashboard template
├── strategies/
│   ├── __init__.py
│   └── moving_average.py    # Moving average strategy
├── utils/
│   ├── __init__.py
│   └── logger.py           # Logging utilities
└── .vscode/                # VS Code configuration
    ├── launch.json
    └── settings.json
```

## Quick Start

### 1. Set up Python Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

1. **Get Bybit API Keys**:
   - Log into Bybit
   - Go to API Management
   - Create new API key with trading permissions
   - **Start with testnet for safety**

2. **Set up configuration**:
   ```powershell
   # Copy example config file
   copy config.example.json config.json
   ```

3. **Update `config.json` with your credentials**:
   ```json
   {
       "api_key": "YOUR_ACTUAL_API_KEY",
       "api_secret": "YOUR_ACTUAL_API_SECRET",
       "testnet": true
   }
   ```

### 3. Run the Bot

**Option 1: Web Dashboard (Recommended)**
```powershell
python start_dashboard.py
```
This will start a beautiful web interface at http://localhost:5000 with:
- Real-time trading dashboard
- Live price charts with moving averages
- Account balance and P&L tracking
- Trading signals and position monitoring
- Trading history

**Option 2: Command Line**
```powershell
python bot.py
```

## Configuration

All bot settings are in `config.json`:

- `api_key`: Your Bybit API key
- `api_secret`: Your Bybit API secret
- `testnet`: Use testnet (true) or mainnet (false)
- `trading_pairs`: List of trading pairs to monitor
- `position_size`: Base position size
- `stop_loss_percentage`: Stop loss percentage (2.0 = 2%)
- `take_profit_percentage`: Take profit percentage (4.0 = 4%)
- `ma_short_period`: Short moving average period
- `ma_long_period`: Long moving average period
- `trading_interval`: Bot cycle interval in seconds

## Strategy

The bot uses a simple moving average crossover strategy:
- **Buy Signal**: When short MA crosses above long MA
- **Sell Signal**: When short MA crosses below long MA

## Risk Management

- Maximum 10% of account balance per position
- Automatic stop loss and take profit
- Position size calculation based on account balance
- Error handling and recovery

## Logging

- Console output for real-time monitoring
- Daily log files in `logs/` directory
- Detailed error logging and debugging

## Safety Notes

⚠️ **Important Safety Guidelines**:

1. **Always test with testnet first**
2. **Start with small position sizes**
3. **Monitor the bot actively initially**
4. **Keep API keys secure**
5. **Review logs regularly**
6. **Understand the risks of automated trading**

## Development

### Running in VS Code

The project includes VS Code configuration:
- Press `F5` to run the bot in debug mode
- Use integrated terminal for commands
- Python environment auto-detection

### Extending the Bot

To add new strategies:
1. Create new strategy class in `strategies/`
2. Implement required methods
3. Update bot to use new strategy

### Dependencies

- `pybit`: Bybit API client
- `pandas`: Data manipulation
- `numpy`: Numerical computations
- `ta`: Technical analysis indicators

## Disclaimer

This trading bot is for educational purposes. Cryptocurrency trading involves significant risk of loss. Use at your own risk and never invest more than you can afford to lose.

## License

This project is open source and available under the MIT License.
