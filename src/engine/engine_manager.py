import importlib
import logging
from typing import Any, Dict 

from ..broker.broker import Broker
from ..broker.broker_mapper import BROKER_MAPPER
from ..strategy.strategy_manager import StrategyManager

from ..config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EngineManager():
    def __init__(self, broker_name: str, strategy_name: str, strategy_parameters: Dict[str, Any]):
        self.broker = self.create_broker(broker_name=broker_name)
        self.strategy_manager = self.create_strategy_manager(strategy_name=strategy_name, strategy_parameters=strategy_parameters)

        logger.info("Engine Manager successfully created.")

    @staticmethod
    def create_broker(broker_name: str) -> Broker:
        try:
            broker_module_path = BROKER_MAPPER[broker_name]["broker_module_path"]
            broker_class_name = BROKER_MAPPER[broker_name]["broker_class_name"]

            module = importlib.import_module(broker_module_path)

            broker_class = getattr(module, broker_class_name)

            if not issubclass(broker_class, Broker):
                raise TypeError(f"Class {broker_class_name} doesn't inherit class Broker.")

            broker = broker_class( 
                            settings.api_key, 
                            settings.secret_key.get_secret_value()
                            )
            
            return broker
             
        except Exception as e:
            logger.critical(f"Error creating broker: {e}")
            raise
    
    @staticmethod
    def create_strategy_manager(strategy_name: str, strategy_parameters: Dict[str, Any]) -> StrategyManager:
        try:
            strategy_manager = StrategyManager()

            strategy_manager.create_strategy( 
                            strategy_name=strategy_name,
                            parameters=strategy_parameters
                            )

            return strategy_manager
             
        except Exception as e:
            logger.critical(f"Error creating strategy manager: {e}")
            raise