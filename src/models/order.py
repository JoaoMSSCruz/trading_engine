from ..common.common import InternalSide

class Order:
    """Internal representation of an order"""

    def __init__(
        self, symbol: str, 
        notional: float, 
        side: InternalSide, 
    ):

        self.symbol = symbol
        self.notional = notional
        self.side = side

    """Getters"""
    def get_symbol(self) -> str:
        return self.symbol
    
    def get_notional(self) -> float:
        return self.notional
    
    def get_side(self) -> InternalSide:
        return self.side

    def __str__(self):
        return f"Symbol: {self.symbol}, Notional: {self.notional}, Side: {self.side.value}"