import importlib
from typing import List, Dict

from ..common.asset_mapper import AssetMapper
from ..common.common import InternalTimeframe
from .data_broker.data_broker import DataBroker
from .data_broker.broker_mapper import BROKER_MAPPER
from ..models.bar import Bar
from ..models.logger import Logger

logger = Logger.logger

class DataManager:
    def __init__(self, 
                broker_name: str, 
                symbols: List[str], 
                timeframe: InternalTimeframe, 
                asset_mapper: AssetMapper,
                **parameters
                ) -> None:
        """Note: For now we can only have 1 data broker"""
        self.broker_name = broker_name
        self.data_broker = self.create_broker(broker_name=broker_name,
                                               **parameters)
        self.symbols = self.convert_symbols(asset_mapper=asset_mapper,
                                            symbols=symbols,
                                            broker_name=broker_name)

        self.timeframe = timeframe

    def get_broker_name(self) -> str:
        return self.broker_name

    @staticmethod
    def convert_symbols(asset_mapper: AssetMapper, 
                        symbols: List[str],
                        broker_name: str
                        ) -> List[str]:
        converted_symbols = list()
        for symbol in symbols:
            converted_symbol = asset_mapper.get_broker_symbol(internal_asset=symbol,
                                                              broker_name=broker_name)
            converted_symbols.append(converted_symbol)
        return converted_symbols

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
                        limit: int) -> Dict[str, List[Bar]]:

        bars = self.data_broker.get_assets_bars(
                    symbols=self.symbols,
                    internal_timeframe=self.timeframe,
                    limit=limit
                )
        
        return bars