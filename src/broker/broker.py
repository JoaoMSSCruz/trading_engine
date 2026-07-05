from abc import ABC, abstractmethod
from typing import Any, List

from ..models.position import Position

class Broker(ABC):
    @abstractmethod
    def get_open_positions(self):
        pass

    @abstractmethod
    def get_asset_price(self, asset_name: str):
        '''TODO: Define a way to inform the interval of time
                A good way would be to have a timeframe and a quantity''' 
        pass

    @abstractmethod
    def send_order(self):
        '''TODO: Use interal class that represent an order
                Have an Order as a parameter''' 
        pass

    @abstractmethod
    def normalize_positions(self, external_positions: List[Any]) -> List[Position]:
        pass