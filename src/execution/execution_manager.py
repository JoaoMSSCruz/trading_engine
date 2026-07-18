import importlib
from typing import List

from .execution_broker.execution_broker import ExecutionBroker

from .execution_broker.mapper import BROKER_MAPPER
from ..models.logger import Logger
from ..models.order import Order

logger = Logger.logger

class ExecutionManager:
    def __init__(self, broker_name: str, **parameters):
        self.execution_broker = self.create_broker(broker_name=broker_name,
                                                   **parameters)

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

    def submit_orders(self, internal_orders: List[Order]) -> None:
        self.execution_broker.submit_orders(internal_orders=internal_orders)