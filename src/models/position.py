class Position:
    """Internal representation of an asset's position in an account"""

    def __init__(self, uid: str, symbol: str, quantity: float):
        self.uid = uid
        self.symbol = symbol
        self.quantity = quantity

    """Getters"""
    def get_uid(self) -> str:
        return self.uid
    
    def get_symbol(self) -> str:
        return self.symbol
    
    def get_quantity(self) -> float:
        return self.quantity

    """Class methods"""
    def __str__(self):
        return f"Symbol: {self.symbol}, Quantity: {self.quantity}"