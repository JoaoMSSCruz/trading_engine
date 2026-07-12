from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ..common import InternalTimeframe
from ..models.bar import Bar
from ..models.order import Order
from ..models.position import Position


class Broker(ABC):
    @abstractmethod
    def __init__(self, api_key: str, secret_key: str):
        pass

    @abstractmethod
    def get_open_positions(self) -> List[Position]:
        pass
    
    @abstractmethod
    def get_assets_bar(self, symbols: List[str], internal_timeframe: InternalTimeframe) -> Dict[str, List[Bar]]:
        pass

    @abstractmethod
    def send_order(self, internal_order: Order) -> None: 
        pass

    @staticmethod
    @abstractmethod
    def normalize_positions(external_positions: List[Any]) -> List[Position]:
        pass