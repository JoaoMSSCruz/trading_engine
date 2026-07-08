from datetime import datetime

class Bar:
    """Internal representation of an asset's bar"""

    def __init__(self, symbol: str, timestamp: datetime,
                 open: float, high: float, low: float,
                 close: float, volume: float):
        self.symbol = symbol
        self.timestamp = timestamp
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    """Getters"""
    def get_symbol(self) -> str:
        return self.symbol
    
    def get_timestamp(self) -> datetime:
        return self.timestamp
    
    def get_open(self) -> float:
        return self.open
    
    def get_high(self) -> float:
        return self.high
    
    def get_low(self) -> float:
        return self.low
    
    def get_close(self) -> float:
        return self.close
    
    def get_volume(self) -> float:
        return self.volume