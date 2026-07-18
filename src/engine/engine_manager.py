import importlib
import time
from typing import Any, Dict, List

from ..data.data_manager import DataManager
from ..common import InternalTimeframe
from ..config import settings
from ..models.logger import Logger
from ..strategy.strategy import Strategy
from ..strategy.strategy_manager import StrategyManager
from ..strategy.strategy_mapper import STRATEGY_MAPPER

logger = Logger.logger

class EngineManager():
    def __init__(self, 
                broker_name: str, 
                timeframe: str, 
                strategy_name: str,
                strategy_lookback: str,
                strategy_parameters: Dict[str, Any],
                symbols: List[str]
                ):
        self.data_manager = self.create_data_manager(broker_name=broker_name)
        self.strategy_manager = self.create_strategy_manager(strategy_name=strategy_name, strategy_parameters=strategy_parameters)
        self.lookback = int(strategy_lookback)
        self.timeframe = InternalTimeframe(timeframe)
        self.symbols = symbols
        
        logger.info("Engine Manager successfully created.")

    @staticmethod
    def create_data_manager(broker_name: str) -> DataManager:
        try:
            broker_credentials = {
                "api_key": settings.api_key,
                "secret_key": settings.secret_key.get_secret_value()
            }
            data_manager = DataManager(broker_name=broker_name,
                                       **broker_credentials)
            
            return data_manager
             
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

    def run(self):
        """TODO: Implement dry run: a run that doesn't have real world consequences,
        basically doesn't buy/sell. This is helpful for debug.
        This entity must be the one storing the bars, and then updating the list for
        each strategy call.
        """
        while True:
            bars = self.data_manager.get_assets_bars(symbols=self.symbols, 
                                                     internal_timeframe=self.timeframe,
                                                     limit=self.lookback)
            
            weights = self.strategy_manager.call_strategy(bars=bars)

            logger.info(f"Weights: {weights}.")
            
            logger.info(f"Sleeping for: {self.timeframe.value}")
            time.sleep(self.timeframe.to_seconds)
            

    