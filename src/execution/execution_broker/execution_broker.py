from abc import ABC, abstractmethod 
from typing import Any, List

from ...models.order import Order
from ...models.position import Position
from ...models.portfolio import Portfolio

class ExecutionBroker(ABC):
    @abstractmethod
    def __init__(self, **parameters):
        pass
    
    def get_portfolio(self) -> Portfolio:
        positions = self.get_positions()
        cash = self.get_cash()
        portfolio = Portfolio(positions=positions,
                              cash=cash)
        return portfolio

    @abstractmethod
    def get_positions(self) -> List[Position]:
        pass

    @abstractmethod
    def get_cash(self) -> float:
        pass

    @abstractmethod
    def submit_orders(self, 
                      internal_orders: List[Order]
                      ) -> None:
        pass 

    @abstractmethod
    def internal_orders_to_broker_orders(self, 
                                         internal_orders: List[Order]
                                         ) -> List[Any]:
        pass

    @abstractmethod
    def broker_positions_to_internal_positions(self, 
                                               broker_positions: List[Any]
                                               ) -> List[Position]:
        pass