from typing import Dict, List

from .position import Position

class Portfolio:
    def __init__(self, 
                positions: List[Position],
                cash: float):
        self.cash = cash
        self.positions = self.positions_to_dict(positions=positions)

    @staticmethod
    def positions_to_dict(positions: List[Position]) -> Dict[str, Position]:
        positions_dict = dict()
        for position in positions:
            positions_dict[position.get_symbol()] = position
        return positions_dict

    def get_position(self, symbol: str) -> Position | None:
        if symbol in self.positions:
            return self.positions[symbol]
        return None

    def get_cash(self) -> float:
        return self.cash
    