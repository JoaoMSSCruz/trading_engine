from ..common import alpaca_side

class Order:
    def __init__(self, symbol: str, quantity: int, side: alpaca_side):
        self.symbol = symbol
        self.quantity = quantity
        self.side = side

    def __str__(self):
        return f"Symbol: {self.symbol}, Quantity: {self.quantity}, Side: {self.side.value}"