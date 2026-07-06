class Position:
    def __init__(self, uid: str, symbol: str, quantity: int):
        self.uid = uid
        self.symbol = symbol
        self.quantity = quantity

    def __str__(self):
        return f"Symbol: {self.symbol}, Quantity: {self.quantity}"