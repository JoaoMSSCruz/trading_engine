from abc import ABC, abstractmethod 
from typing import Any, List

from ...models.order import Order

class ExecutionBroker(ABC):
    @abstractmethod
    def __init__(self, **parameters):
        pass

    @abstractmethod
    def submit_orders(self, 
                      internal_orders: List[Order]
                      ) -> None:
        pass 

    @abstractmethod
    def internal_orders_to_broker_orders(self, internal_orders: List[Order]) -> List[Any]:
        pass