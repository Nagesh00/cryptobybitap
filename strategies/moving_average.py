import pandas as pd
import numpy as np
from utils.logger import setup_logger

class MovingAverageStrategy:
    def __init__(self, short_period=20, long_period=50):
        self.short_period = short_period
        self.long_period = long_period
        self.logger = setup_logger("MovingAverageStrategy")
        
    def calculate_signals(self, df):
        """Calculate moving average signals"""
        try:
            # Calculate moving averages
            df['ma_short'] = df['close'].rolling(window=self.short_period).mean()
            df['ma_long'] = df['close'].rolling(window=self.long_period).mean()
            
            # Generate signals
            df['signal'] = 0
            df['signal'][self.short_period:] = np.where(
                df['ma_short'][self.short_period:] > df['ma_long'][self.short_period:], 1, 0
            )
            df['position'] = df['signal'].diff()
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error calculating signals: {e}")
            return None
    
    def get_current_signal(self, data):
        """Get current trading signal"""
        try:
            df = self.prepare_dataframe(data)
            if df is None or len(df) < self.long_period:
                return None, None, None
            
            # Calculate signals
            df = self.calculate_signals(df)
            if df is None:
                return None, None, None
            
            # Get latest values
            latest = df.iloc[-1]
            previous = df.iloc[-2] if len(df) > 1 else None
            
            signal = None
            if previous is not None:
                if latest['position'] == 1.0:  # Buy signal
                    signal = "BUY"
                elif latest['position'] == -1.0:  # Sell signal
                    signal = "SELL"
            
            return signal, latest['ma_short'], latest['ma_long']
            
        except Exception as e:
            self.logger.error(f"Error getting current signal: {e}")
            return None, None, None
    
    def prepare_dataframe(self, kline_data):
        """Convert kline data to DataFrame"""
        try:
            if not kline_data or 'result' not in kline_data:
                return None
            
            data = []
            for kline in kline_data['result']['list']:
                data.append({
                    'timestamp': int(kline[0]),
                    'open': float(kline[1]),
                    'high': float(kline[2]),
                    'low': float(kline[3]),
                    'close': float(kline[4]),
                    'volume': float(kline[5])
                })
            
            df = pd.DataFrame(data)
            df = df.sort_values('timestamp').reset_index(drop=True)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error preparing dataframe: {e}")
            return None
