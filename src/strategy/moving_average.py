from typing import Any, List

from ..models.bar import Bar
from .strategy import Strategy

class MovingAverage(Strategy):
    def __init__(self, period: int, symbol: str):
        self.period = period
        self.symbol = symbol

    def run_strategy(self, bars: List[Bar]) -> Any:
        """TODO: Implement this"""
        pass