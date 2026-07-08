import importlib
import logging
from typing import List

from ..models.bar import Bar
from .strategy import Strategy
from .strategy_mapper import STRATEGY_MAPPER

logger = logging.getLogger(__name__)

class StrategyManager:
    """Entity that manages the internal strategies"""
    
    def __init__(self):
        self.strategy: Strategy | None = None

    def create_strategy(self, strategy_name: str, **parameters):
        """We will assume that there will only be one instance of a Strategy"""
        try:
            strategy_module_path = STRATEGY_MAPPER[strategy_name]["strategy_module_path"]
            strategy_class_name = STRATEGY_MAPPER[strategy_name]["strategy_class_name"]

            module = importlib.import_module(strategy_module_path)

            strategy_class = getattr(module, strategy_class_name)

            if not issubclass(strategy_class, Strategy):
                raise TypeError(f"Class {strategy_class_name} doesn't inherit class Strategy.")

            strategy_instance = strategy_class(**parameters)


            self.strategy = strategy_instance

            logger.info(f"Strategy {strategy_class_name} successfully created.")
             
        except Exception as e:
            logger.critical(f"Error creating strategy: {e}")
            raise

    def call_strategy(self, bars: List[Bar]):
        """TODO: Return internal representation of strategy output"""
        if not self.strategy:
            raise RuntimeError("Calling strategy not yet created.")
        
        return self.strategy.run_strategy(bars=bars)

            