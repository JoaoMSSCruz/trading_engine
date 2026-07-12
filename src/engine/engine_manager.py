import importlib
import logging
from typing import Any, Dict 
import timeframe

from ..broker.broker import Broker
from ..broker.broker_mapper import BROKER_MAPPER
from ..common import InternalTimeframe
from ..strategy.strategy import Strategy
from ..strategy.strategy_manager import StrategyManager
from ..strategy.strategy_mapper import STRATEGY_MAPPER

from ..config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EngineManager():
    def __init__(self, 
                broker_name: str, 
                timeframe: str, 
                strategy_name: str,
                strategy_parameters: Dict[str, Any]
                ):
        # TODO 15: Add timeframe, which is in the config's execution
        self.broker = self.create_broker(broker_name=broker_name)
        self.strategy_manager = self.create_strategy_manager(strategy_name=strategy_name, strategy_parameters=strategy_parameters)
        self.timeframe = InternalTimeframe(timeframe)

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
            strategy_module_path = STRATEGY_MAPPER[strategy_name]["strategy_module_path"]
            strategy_class_name = STRATEGY_MAPPER[strategy_name]["strategy_class_name"]

            module = importlib.import_module(strategy_module_path)

            strategy_class = getattr(module, strategy_class_name)

            if not issubclass(strategy_class, Strategy):
                raise TypeError(f"Class {strategy_class_name} doesn't inherit class Strategy.")


            strategy_manager = StrategyManager(
                strategy_class=strategy_class,
                parameters=strategy_parameters
                )

            return strategy_manager
             
        except Exception as e:
            logger.critical(f"Error creating strategy manager: {e}")
            raise

    """ TODO 15: Create method that sleeps for [timeframe] and then wakes the strategy.
        It might be a method "run" who calls a sleep method.
    """

    