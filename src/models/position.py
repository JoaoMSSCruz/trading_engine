class Position:
    def __init__(self, uid: str, symbol: str, quantity: float):
        self.uid = uid
        self.symbol = symbol
        self.quantity = quantity

    def get_uid(self) -> str:
        return self.uid
    
    def get_symbol(self) -> str:
        return self.symbol
    
    def get_quantity(self) -> float:
        return self.quantity

    def __str__(self):
        return f"Symbol: {self.symbol}, Quantity: {self.quantity}"