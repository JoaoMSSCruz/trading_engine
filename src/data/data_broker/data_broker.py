from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ...common.common import InternalTimeframe
from ...models.bar import Bar

class DataBroker(ABC):
    @abstractmethod
    def __init__(self, **parameters):
        pass

    @abstractmethod
    def create_historical_data_client(self):
        pass

    @abstractmethod
    def create_data_stream_client(self):
        pass

    @abstractmethod
    def connect_data_stream(self):
        pass

    @abstractmethod
    def desconnect_data_stream(self):
        pass

    @abstractmethod
    def get_assets_bars(self, 
                        symbols: List[str],
                        internal_timeframe: InternalTimeframe,
                        limit: int
                        ) -> Dict[str, List[Bar]]:
        pass

    @staticmethod
    @abstractmethod
    def broker_bars_to_internal_bars(bars: List[Any]) -> List[Bar]:
        pass