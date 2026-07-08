from abc import ABC, abstractmethod
from typing import Any, List

from ..models.bar import Bar

class Strategy(ABC):
    """Abstract representation of a Strategy"""

    def __init__(self, strategy_name: str):
        self.strategy_name = strategy_name

    @abstractmethod
    def run_strategy(self, bars: List[Bar]) -> Any:
        """TODO: Define the internal representation of the output of a strategy
            It should be a class Weights or something similar
        """
        pass
