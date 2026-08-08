import time
from typing import Any, Dict, List

from ..data.data_manager import DataManager
from ..common.asset_mapper import AssetMapper 
from ..common.common import InternalTimeframe
from ..config import settings
from ..execution.execution_manager import ExecutionManager
from ..models.logger import Logger
from ..strategy.strategy_manager import StrategyManager

logger = Logger.logger

class EngineManager():
    def __init__(self, 
                asset_mapper: AssetMapper,
                data_broker_name: str, 
                data_timeframe: str, 
                strategy_name: str,
                strategy_lookback: str,
                strategy_parameters: Dict[str, Any],
                symbols: List[str],
                execution_broker_name: str,
                ):
        self.data_manager = self.create_data_manager(
                                broker_name=data_broker_name, 
                                symbols=symbols,
                                data_timeframe=InternalTimeframe(data_timeframe),
                                asset_mapper=asset_mapper
                            )
        self.strategy_manager = self.create_strategy_manager(
                                    strategy_name=strategy_name,
                                    **strategy_parameters
                                )
        self.lookback = int(strategy_lookback)
        self.execution_manager = self.create_execution_manager(broker_name=execution_broker_name,
                                                               asset_mapper=asset_mapper)

        self.timeframe = InternalTimeframe(data_timeframe)
        
        logger.info("Engine Manager successfully created.")

    @staticmethod
    def create_data_manager(
        broker_name: str,
        symbols: List[str], 
        data_timeframe: InternalTimeframe,
        asset_mapper: AssetMapper
        ) -> DataManager:
        try:
            broker_credentials = {
                "api_key": settings.api_key,
                "secret_key": settings.secret_key.get_secret_value()
            }
            data_manager = DataManager(
                            broker_name=broker_name,
                            symbols=symbols,
                            timeframe=data_timeframe,
                            asset_mapper=asset_mapper,
                            **broker_credentials
                            )
            
            return data_manager
             
        except Exception as e:
            logger.critical(f"Error creating data broker: {e}")
            raise
    
    @staticmethod
    def create_strategy_manager(strategy_name: str, **strategy_parameters) -> StrategyManager:
        try:    
            strategy_manager = StrategyManager(strategy_name=strategy_name,
                                               **strategy_parameters)

            return strategy_manager
             
        except Exception as e:
            logger.critical(f"Error creating strategy manager: {e}")
            raise

    @staticmethod
    def create_execution_manager(broker_name:str, asset_mapper: AssetMapper
                                ) -> ExecutionManager:
        try:
            broker_credentials = {
                "api_key": settings.api_key,
                "secret_key": settings.secret_key.get_secret_value()
            }
            execution_manager = ExecutionManager(broker_name=broker_name,
                                                 asset_mapper=asset_mapper,
                                                 **broker_credentials
                                                 )
            
            return execution_manager
        except Exception as e:
            logger.critical(f"Error creating execution broker: {e}")
            raise

    def start_engine(self):
        """TODO: Implement dry run: a run that doesn't have real world consequences,
        basically doesn't buy/sell. This is helpful for debug.
        This entity must be the one storing the bars, and then updating the list for
        each strategy call.
            TODO: Implement a warmup. For this I will need to implement WebSocket.
        """
        while True:
            logger.info("Starting Run Cycle:")
            bars = self.data_manager.get_assets_bars(limit=self.lookback)
            
            weights = self.strategy_manager.call_strategy(bars=bars)

            logger.info(f"Weights: {weights}.")

            self.execution_manager.execute(
                                    weights=weights, 
                                    bars=bars,
                                    data_broker=self.data_manager.get_broker_name(),
                                )
            
            logger.info(f"Sleeping for: {self.timeframe.value}")
            time.sleep(self.timeframe.to_seconds)

            

    