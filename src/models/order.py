from ..common import alpaca_side

class Order:
    def __init__(self, symbol: str, quantity: float, side: alpaca_side):
        self.symbol = symbol
        self.quantity = quantity
        self.side = side

    def get_symbol(self) -> str:
        return self.symbol
    
    def def_quantity(self) -> float:
        return self.quantity
    
    def get_side(self) -> alpaca_side:
        return self.side

    def __str__(self):
        return f"Symbol: {self.symbol}, Quantity: {self.quantity}, Side: {self.side.value}"