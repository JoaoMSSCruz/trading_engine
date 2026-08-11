import importlib
from typing import List, Dict

from ..common.asset_mapper import AssetMapper
from ..common.common import InternalTimeframe
from ..config import settings
from .data_broker.data_broker import DataBroker
from .data_broker.broker_mapper import BROKER_MAPPER
from .database.connection import DatabaseManager
from .database.repository import MarketDataRepository
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
        self.database_manager = self.create_database_manager()
        self.market_data_repository = self.create_market_data_repository(database_manager=self.database_manager) 

    def get_broker_name(self) -> str:
        return self.broker_name

    @staticmethod
    def create_database_manager() -> DatabaseManager:
        database_user = settings.postgres_user
        database_password = settings.postgres_password
        data_base_db = settings.postgres_db

        database_url = f"postgresql://{database_user}:{database_password}@postgres-db:5432/{data_base_db}"

        database_manager = DatabaseManager(db_url=database_url)

        database_manager.connect()

        return database_manager

    @staticmethod
    def create_market_data_repository(database_manager: DatabaseManager) -> MarketDataRepository:
        return MarketDataRepository(db_manager=database_manager)

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
                        limit: int
                        ) -> Dict[str, List[Bar]]:

        bars = self.data_broker.get_assets_bars(
                    symbols=self.symbols,
                    internal_timeframe=self.timeframe,
                    limit=limit
                )

        for symbol_bars in bars.values():
            self.add_bar_to_db(symbol_bars) 
        
        return bars

    def add_bar_to_db(self, bars: List[Bar]) -> None:
        for bar in bars:
            self.market_data_repository.save_bar(
                symbol=bar.get_symbol(),
                timestamp=bar.get_timestamp(),
                open_p=bar.get_open(),
                high=bar.get_high(),
                low=bar.get_low(),
                close=bar.get_close(),
                volume=bar.get_volume()
            )