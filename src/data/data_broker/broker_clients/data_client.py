from abc import ABC, abstractmethod
from typing import Any, Dict, List

class DataClient(ABC):
    @abstractmethod
    def __init__(self, symbols: List[str], timeframe: Any):
        self.symbols = symbols
        self.timeframe = timeframe

    @abstractmethod
    def load_warmup(self, ) -> Dict[str, List[Any]]:
        pass

    @abstractmethod
    def get_latest(self) -> Dict[str, Any]:
        pass

