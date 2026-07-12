import logging
from typing import Any, Dict, List

from ..models.bar import Bar
from .strategy import Strategy

logger = logging.getLogger(__name__)

class StrategyManager:
    """Entity that manages the internal strategies"""
    
    def __init__(self, strategy_class: type[Strategy], parameters: Dict[str, Any]):
        self.create_strategy(strategy_class=strategy_class, parameters=parameters)
        logger.info("Strategy Manager successfully created.")

    def create_strategy(self, strategy_class: type[Strategy], parameters: Dict[str, Any]):
        """We will assume that there will only be one instance of a Strategy"""
        try:

            strategy_instance = strategy_class(**parameters)


            self.strategy = strategy_instance

            logger.info(f"Strategy {strategy_class} successfully created.")
             
        except Exception as e:
            logger.critical(f"Error creating strategy: {e}")
            raise

    def call_strategy(self, bars: List[Bar]):
        """TODO: Return internal representation of strategy output"""
        if not self.strategy:
            raise RuntimeError("Calling strategy not yet created.")
        
        return self.strategy.get_weights(bars=bars)

            