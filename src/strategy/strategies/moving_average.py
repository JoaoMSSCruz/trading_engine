from typing import Dict, List

from ...models.bar import Bar
from ...models.weights import Weights
from .strategy import Strategy

class MovingAverage(Strategy):
    def __init__(self, threshold: int):
        self.threshold = threshold

    def get_weights(self, bars: Dict[str, List[Bar]]) -> Weights:
        """There is only one asset being dealt in this strategy"""
        symbol_price_sum = 0
        counter = 0
        for symbol in bars.keys():
            """Iterating even tho theres only one symbol"""
            moving_average_symbol = symbol
            symbol_bars = bars[moving_average_symbol]
            for bar in symbol_bars:
                symbol_price_sum += bar.get_close()
                counter += 1
        moving_average = symbol_price_sum / counter
        if bar.get_close() > moving_average * self.threshold:
            weight = 1
        else:
            weight = 0
        
        return Weights(weights={moving_average_symbol: weight})