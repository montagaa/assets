"""Technical indicator calculation utilities."""

from typing import Iterable
import pandas as pd
import ta  # from TA-Lib wrapper


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add common indicators to the dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with a `close` price column.

    Returns
    -------
    pd.DataFrame
        DataFrame extended with indicator columns.
    """
    indicators = pd.DataFrame(index=df.index)

    # Basic indicators
    indicators["ma_14"] = ta.trend.sma_indicator(df["close"], window=14)
    indicators["ema_14"] = ta.trend.ema_indicator(df["close"], window=14)
    indicators["rsi_14"] = ta.momentum.rsi(df["close"], window=14)
    indicators["macd"] = ta.trend.macd(df["close"])

    # Additional indicators for improved predictions
    indicators["bb_upper"] = ta.volatility.bollinger_hband(df["close"], window=20, window_dev=2)
    indicators["bb_lower"] = ta.volatility.bollinger_lband(df["close"], window=20, window_dev=2)

    return indicators
