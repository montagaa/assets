"""Demo account trading utilities."""

from typing import Optional

try:
    from iqoptionapi.stable_api import IQ_Option
except ImportError:  # pragma: no cover - library may not be installed in tests
    IQ_Option = None  # type: ignore


class DemoTrader:
    """Handle connection to IQ Option for demo trading."""

    def __init__(self, username: str, password: str) -> None:
        if IQ_Option is None:
            raise ImportError(
                "iqoptionapi package required for trading functionality"
            )
        self.api = IQ_Option(username, password)
        self.api.connect()
        self.api.change_balance("PRACTICE")

    def buy(
        self, pair: str, direction: str, amount: float, duration: int = 3
    ) -> Optional[tuple]:
        """Place a trade on the demo account."""
        if direction.lower() not in {"call", "put"}:
            raise ValueError("direction must be 'call' or 'put'")
        return self.api.buy(amount, pair, direction, duration)

    def close(self) -> None:
        """Close the API connection."""
        self.api.close()
