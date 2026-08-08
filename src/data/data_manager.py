import importlib
from typing import List, Dict

from ..common.common import InternalTimeframe
from .data_broker.data_broker import DataBroker
from .data_broker.broker_mapper import BROKER_MAPPER
from ..models.bar import Bar
from ..models.logger import Logger

logger = Logger.logger

class DataManager:
    def __init__(self, broker_name: str, timeframe: InternalTimeframe, **parameters):
        self.data_broker = self.create_broker(broker_name=broker_name,
                                               **parameters)
        self.timeframe = timeframe

    @staticmethod
    def create_broker(broker_name: str, **parameters) -> DataBroker:
        try:
            broker_module_path = BROKER_MAPPER[broker_name]["data_broker_module_path"]
            broker_class_name = BROKER_MAPPER[broker_name]["data_broker_class_name"]

            module = importlib.import_module(broker_module_path)

            broker_class = getattr(module, broker_class_name)

            if not issubclass(broker_class, DataBroker):
                raise TypeError(f"Class {broker_class_name} doesn't inherit class Broker.")

            broker = broker_class(**parameters)
            
            return broker
             
        except Exception as e:
            logger.critical(f"Error creating broker: {e}")
            raise

    def get_assets_bars(self, 
                        symbols: List[str],
                        limit: int) -> Dict[str, List[Bar]]:

        bars = self.data_broker.get_assets_bars(symbols=symbols,
                                         internal_timeframe=self.timeframe,
                                         limit=limit)
        
        return bars