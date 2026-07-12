from abc import ABC, abstractmethod
from typing import Dict, List

from ..models.bar import Bar
from ..models.weights import Weights

class Strategy(ABC):
    """Abstract representation of a Strategy"""

    def __init__(self, **parameters):
        pass

    @abstractmethod
    def get_weights(self, bars: Dict[str, List[Bar]]) -> Weights:
        """TODO: Define the internal representation of the output of a strategy
            It should be a class Weights or something similar
        """
        pass
