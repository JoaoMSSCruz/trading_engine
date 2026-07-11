from abc import ABC, abstractmethod
from typing import Any, List

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
    def get_asset_bars(self, symbol: str, internal_timeframe: InternalTimeframe) -> List[Bar]:
        '''TODO: Perhaps quantity or lookback would be necessary''' 
        pass

    @abstractmethod
    def send_order(self, internal_order: Order) -> None: 
        pass

    @staticmethod
    @abstractmethod
    def normalize_positions(external_positions: List[Any]) -> List[Position]:
        pass