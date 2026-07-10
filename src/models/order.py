from ..common import InternalSide

class Order:
    """Internal representation of an order"""

    def __init__(self, symbol: str, quantity: float, side: InternalSide):
        self.symbol = symbol
        self.quantity = quantity
        self.side = side

    """Getters"""
    def get_symbol(self) -> str:
        return self.symbol
    
    def get_quantity(self) -> float:
        return self.quantity
    
    def get_side(self) -> InternalSide:
        return self.side

    def __str__(self):
        return f"Symbol: {self.symbol}, Quantity: {self.quantity}, Side: {self.side.value}"