from typing import Any, List

from ..models.bar import Bar
from .strategy import Strategy

class MovingAverage(Strategy):
    def __init__(self, lookback: int, symbol: str):
        self.lookback = lookback
        self.symbol = symbol

    def get_weights(self, bars: List[Bar]) -> Any:
        """TODO: Implement this"""
        pass