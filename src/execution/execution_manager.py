import importlib
from typing import List

from .execution_broker.execution_broker import ExecutionBroker

from .execution_broker.mapper import BROKER_MAPPER
from ..models.logger import Logger
from ..models.order import Order
from ..models.portfolio import Portfolio
from ..models.weights import Weights

logger = Logger.logger

class ExecutionManager:
    def __init__(self, broker_name: str, **parameters):
        self.execution_broker = self.create_broker(broker_name=broker_name,
                                                   **parameters)
        self.portfolio = self.get_portfolio()

    @staticmethod
    def create_broker(broker_name: str, **parameters) -> ExecutionBroker:
        try:
            broker_module_path = BROKER_MAPPER[broker_name]["execution_broker_module_path"]
            broker_class_name = BROKER_MAPPER[broker_name]["execution_broker_class_name"]

            module = importlib.import_module(broker_module_path)

            broker_class = getattr(module, broker_class_name)

            if not issubclass(broker_class, ExecutionBroker):
                raise TypeError(f"Class {broker_class_name} doesn't inherit class Broker.")

            broker = broker_class(**parameters)
            
            return broker
             
        except Exception as e:
            logger.critical(f"Error creating broker: {e}")
            raise

    def get_portfolio(self) -> Portfolio:
        return self.execution_broker.get_portfolio()

    def execute(self, weights: Weights) -> None:
        orders = self.weights_to_orders(weights=weights)
        self.submit_orders(orders=orders)

    def weights_to_orders(self, weights) -> List[Order]:
        pass

    def submit_orders(self, orders: List[Order]) -> None:
        self.execution_broker.submit_orders(internal_orders=orders)