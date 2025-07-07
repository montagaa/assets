"""Configuration for the trading bot."""

# Telegram bot token provided by BotFather
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# IQ Option credentials
IQ_OPTION_USERNAME = "you@example.com"
IQ_OPTION_PASSWORD = "your_password"

# Trading pair and prediction horizon (e.g., EURUSD for 3-minute prediction)
DEFAULT_PAIR = "EURUSD-OTC"
PREDICTION_HORIZON_MINUTES = 3

# Trade configuration
# Amount to invest per trade on the demo account
TRADE_AMOUNT = 1.0

# Minimum probability required to automatically place a trade
TRADE_CONFIDENCE_THRESHOLD = 0.7
