import pandas as pd
import numpy as np

class MarketAnalyst:
    def __init__(self):
        self.rsi_window = 14  # Standard RSI window
        self.sma_windows = [3, 5]  # Short-term SMAs
        self.ema_windows = [5, 10]  # Medium-term EMAs

    def _validate_data(self, closes):
        """Ensure data quality before analysis"""
        if len(closes) < 2:
            raise ValueError("Insufficient data points")
        if any(price <= 0 for price in closes):
            raise ValueError("Invalid prices (zero or negative)")
        return np.array(closes)

    def calculate_rsi(self, closes):
        """Calculate Relative Strength Index"""
        closes = self._validate_data(closes)
        if len(closes) < self.rsi_window:
            return None
            
        deltas = np.diff(closes)
        gains = deltas.copy()
        losses = deltas.copy()
        gains[gains < 0] = 0
        losses[losses > 0] = 0
        
        avg_gain = pd.Series(gains).rolling(self.rsi_window).mean().values
        avg_loss = pd.Series(-losses).rolling(self.rsi_window).mean().values
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi[-1], 2)

    def calculate_sma(self, closes, window):
        """Simple Moving Average"""
        closes = self._validate_data(closes)
        return round(pd.Series(closes).rolling(window).mean().iloc[-1], 4)

    def calculate_ema(self, closes, window):
        """Exponential Moving Average"""
        closes = self._validate_data(closes)
        return round(pd.Series(closes).ewm(span=window, adjust=False).mean().iloc[-1], 4)

    def calculate_macd(self, closes):
        """Moving Average Convergence Divergence"""
        closes = self._validate_data(closes)
        if len(closes) < 26:
            return None
            
        ema12 = pd.Series(closes).ewm(span=12, adjust=False).mean()
        ema26 = pd.Series(closes).ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        return {
            "macd": round(macd.iloc[-1], 4),
            "signal": round(signal.iloc[-1], 4)
        }

    def analyze_trends(self, historical_prices):
        try:
            # Convert historical prices to DataFrame for easier manipulation
            df = pd.DataFrame(historical_prices)
            
            # Ensure data is sorted chronologically
            df['Start'] = pd.to_datetime(df['Start'])
            df = df.sort_values('Start')
            
            # Extract closing prices
            closes = df['Close'].values
            
            # Basic price analysis
            price_change_pct = ((closes[-1] - closes[0]) / closes[0]) * 100
            recent_trend = "up" if closes[-1] > closes[-2] else "down"
            
            # Calculate technical indicators
            analysis = {
                "price_change": f"{price_change_pct:.2f}%",
                "current_price": closes[-1],
                "recent_trend": recent_trend,
                "sma": {w: self.calculate_sma(closes, w) for w in self.sma_windows},
                "ema": {w: self.calculate_ema(closes, w) for w in self.ema_windows},
                "rsi": self.calculate_rsi(closes),
                "macd": self.calculate_macd(closes)
            }
            
            # Add trend strength analysis
            analysis['trend_strength'] = self._assess_trend_strength(analysis)
            
            return analysis
            
        except Exception as e:
            return {"error": str(e)}

    def _assess_trend_strength(self, analysis):
        """Evaluate trend strength based on multiple indicators"""
        strength = []
        
        # RSI analysis
        if analysis['rsi']:
            if analysis['rsi'] > 70:
                strength.append('Overbought (RSI >70)')
            elif analysis['rsi'] < 30:
                strength.append('Oversold (RSI <30)')
        
        # MACD analysis
        if analysis['macd']:
            if analysis['macd']['macd'] > analysis['macd']['signal']:
                strength.append('Bullish MACD crossover')
            else:
                strength.append('Bearish MACD crossover')
        
        # EMA crossover analysis
        if analysis['ema'][5] and analysis['ema'][10]:
            if analysis['ema'][5] > analysis['ema'][10]:
                strength.append('Bullish EMA crossover (5>10)')
            else:
                strength.append('Bearish EMA crossover (5<10)')
        
        return strength if strength else ['No strong trend indicators']