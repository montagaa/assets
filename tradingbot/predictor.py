"""Prediction model using scikit-learn."""

from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier

from .indicators import compute_indicators


class PricePredictor:
    """A simple price movement predictor."""

    def __init__(self) -> None:
        self.model = LogisticRegression()
        self.is_trained = False

    def train(self, df: pd.DataFrame) -> None:
        """Train the model using historical price data."""
        features = compute_indicators(df)
        features = features.dropna()
        X = features.values
        # Generate labels: 1 if next close is higher else 0
        y = (df["close"].shift(-1).loc[features.index] > df["close"].loc[features.index]).astype(int)
        self.model.fit(X, y)
        self.is_trained = True

    def predict(self, df: pd.DataFrame) -> Tuple[float, int]:
        """Predict the probability of price going up."""
        if not self.is_trained:
            raise RuntimeError("Model must be trained before prediction")

        features = compute_indicators(df).iloc[[-1]].dropna()
        if features.empty:
            raise ValueError("Not enough data for indicators")

        prob = self.model.predict_proba(features.values)[0][1]
        label = int(prob > 0.5)
        return prob, label


class AdvancedPricePredictor:
    """A more sophisticated price movement predictor using gradient boosting."""

    def __init__(self, n_estimators: int = 200) -> None:
        self.model = GradientBoostingClassifier(n_estimators=n_estimators)
        self.is_trained = False

    def train(self, df: pd.DataFrame) -> None:
        """Train the gradient boosting model on historical data."""
        features = compute_indicators(df)
        features = features.dropna()
        X = features.values
        y = (
            df["close"].shift(-1).loc[features.index]
            > df["close"].loc[features.index]
        ).astype(int)
        self.model.fit(X, y)
        self.is_trained = True

    def predict(self, df: pd.DataFrame) -> Tuple[float, int]:
        """Predict price direction using the trained model."""
        if not self.is_trained:
            raise RuntimeError("Model must be trained before prediction")

        features = compute_indicators(df).iloc[[-1]].dropna()
        if features.empty:
            raise ValueError("Not enough data for indicators")

        prob = self.model.predict_proba(features.values)[0][1]
        label = int(prob > 0.5)
        return prob, label
