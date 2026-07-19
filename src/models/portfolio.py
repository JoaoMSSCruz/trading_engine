from typing import List

from .position import Position

class Portfolio:
    def __init__(self, 
                positions: List[Position],
                cash: float):
        self.cash = cash
        self.positions = positions

    def get_positions(self) -> List[Position]:
        return self.positions

    def get_cash(self) -> float:
        return self.cash