import importlib
from typing import Dict, List

from ..models.bar import Bar
from ..models.logger import Logger
from ..models.weights import Weights
from .strategies.strategy import Strategy
from .strategies.strategy_mapper import STRATEGY_MAPPER

logger = Logger.logger

class StrategyManager:
    """Entity that manages the internal strategies"""
    
    def __init__(self, strategy_name: str, **parameters):
        self.strategy = self.create_strategy(strategy_name=strategy_name, **parameters)
        logger.info("Strategy Manager successfully created.")

    def create_strategy(self, strategy_name: str, **parameters) -> Strategy:
        """We will assume that there will only be one instance of a Strategy"""
        try:
            strategy_module_path = STRATEGY_MAPPER[strategy_name]["strategy_module_path"]
            strategy_class_name = STRATEGY_MAPPER[strategy_name]["strategy_class_name"]

            module = importlib.import_module(strategy_module_path)

            strategy_class = getattr(module, strategy_class_name)

            if not issubclass(strategy_class, Strategy):
                raise TypeError(f"Class {strategy_class_name} doesn't inherit class Strategy.")


            strategy = strategy_class(**parameters)

            return strategy
             
        except Exception as e:
            logger.critical(f"Error creating strategy: {e}")
            raise

    def call_strategy(self, bars: Dict[str, List[Bar]]) -> Weights:
        """TODO: Return internal representation of strategy output"""
        """TODO: Implement a initial setup of a strategy"""
        if not self.strategy:
            raise RuntimeError("Calling strategy not yet created.")
        if not bars:
            #FIXME: Create error handling
            logger.warning("No weights available.")
        
        return self.strategy.get_weights(bars=bars)

            