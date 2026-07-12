from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ..models.bar import Bar

class Strategy(ABC):
    """Abstract representation of a Strategy"""

    def __init__(self, **parameters):
        pass

    @abstractmethod
    def get_weights(self, bars: Dict[str, List[Bar]]) -> Any:
        """TODO: Define the internal representation of the output of a strategy
            It should be a class Weights or something similar
        """
        pass
