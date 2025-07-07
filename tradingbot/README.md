# Forex Prediction Trading Bot

This is a sample prototype of a trading bot that connects to IQ Option's WebSocket API, processes
market data using common technical indicators, and provides predictions through a Telegram bot.

## Features

* Connects to IQ Option WebSocket for real-time price updates.
* Calculates multiple indicators (moving average, EMA, RSI, MACD, Bollinger Bands).
* Uses a machine learning model (gradient boosting) to predict short-term price movement.
* Integrates with a Telegram bot to send commands and receive predictions.
* Example UI buttons for quick access to common features.
* Includes an advanced model that can be retrained with your historical data for better accuracy.
* Can place demo trades automatically when confidence is high.

> **Disclaimer:** This code is a simplified demonstration and does not guarantee any level of
> accuracy. Use at your own risk and test thoroughly before trading with real funds.

## Setup

1. Install Python 3.8+ and the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a Telegram bot with [BotFather](https://t.me/botfather) and obtain the API token.
3. Update `config.py` with your Telegram token, IQ Option credentials, and desired trade settings.
4. Run the bot:
   ```bash
   python main.py
   ```

## Notes

* The machine learning model is trained on sample data (`sample_data.csv`). Replace this with your
  own historical price data to improve results.
* IQ Option may have usage limits and restrictions. Ensure you comply with their terms of service.
* Automated trading carries risk. This project is for educational purposes.
* Demo trades are executed only when the prediction probability exceeds the configured threshold.
