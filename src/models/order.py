from ..common import InternalSide, InternalTimeframe

class Order:
    """Internal representation of an order"""

    def __init__(
        self, symbol: str, 
        quantity: float, 
        side: InternalSide, 
        timeframe: InternalTimeframe):

        self.symbol = symbol
        self.quantity = quantity
        self.side = side
        self.timeframe = timeframe

    """Getters"""
    def get_symbol(self) -> str:
        return self.symbol
    
    def get_quantity(self) -> float:
        return self.quantity
    
    def get_side(self) -> InternalSide:
        return self.side
    
    def get_timeframe(self) -> InternalTimeframe:
        return self.timeframe

    def __str__(self):
        return f"Symbol: {self.symbol}, Quantity: {self.quantity}, Side: {self.side.value}, Timeframe: {self.timeframe}"