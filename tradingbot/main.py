"""Entry point for the Telegram trading bot."""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

import pandas as pd
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackContext, CommandHandler

from .config import (
    TELEGRAM_TOKEN,
    IQ_OPTION_USERNAME,
    IQ_OPTION_PASSWORD,
    DEFAULT_PAIR,
    PREDICTION_HORIZON_MINUTES,
    TRADE_AMOUNT,
    TRADE_CONFIDENCE_THRESHOLD,
)
from .predictor import AdvancedPricePredictor
from .trader import DemoTrader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TradingSession:
    predictor: AdvancedPricePredictor
    price_data: pd.DataFrame
    trader: DemoTrader


def load_sample_data() -> pd.DataFrame:
    """Load sample historical prices from CSV."""
    try:
        df = pd.read_csv("sample_data.csv")
    except FileNotFoundError:
        logger.warning("sample_data.csv not found; using dummy data")
        df = pd.DataFrame({"close": [1, 1.1, 1.05, 1.2, 1.15, 1.3]})
    return df


def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message and show buttons."""
    keyboard = [[InlineKeyboardButton("Predict", callback_data="predict")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome to the trading bot!", reply_markup=reply_markup)


def predict(update: Update, context: CallbackContext) -> None:
    """Perform prediction using the latest price data."""
    session: TradingSession = context.bot_data.get("session")
    if not session:
        update.callback_query.message.reply_text("Model not trained yet.")
        return
    try:
        prob, label = session.predictor.predict(session.price_data)
        direction = "UP" if label else "DOWN"
        update.callback_query.message.reply_text(
            f"Prediction for {DEFAULT_PAIR} in {PREDICTION_HORIZON_MINUTES}m: {direction} ({prob:.2%})"
        )
        if prob >= TRADE_CONFIDENCE_THRESHOLD:
            trade_dir = "call" if label else "put"
            session.trader.buy(
                DEFAULT_PAIR, trade_dir, TRADE_AMOUNT, PREDICTION_HORIZON_MINUTES
            )
            update.callback_query.message.reply_text("Demo trade placed")
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception(exc)
        update.callback_query.message.reply_text("Error during prediction")


def main() -> None:
    """Start the Telegram bot and train the model."""
    predictor = AdvancedPricePredictor()
    df = load_sample_data()
    predictor.train(df)

    trader = DemoTrader(IQ_OPTION_USERNAME, IQ_OPTION_PASSWORD)

    session = TradingSession(predictor=predictor, price_data=df, trader=trader)

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("predict", predict))
    application.bot_data["session"] = session

    logger.info("Bot started")
    try:
        application.run_polling()
    finally:
        trader.close()


if __name__ == "__main__":
    main()
