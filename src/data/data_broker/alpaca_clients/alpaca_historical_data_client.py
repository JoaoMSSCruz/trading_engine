from typing import Dict, List

from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.models.bars import Bar, BarSet
from alpaca.data.requests import CryptoBarsRequest, CryptoLatestBarRequest
from alpaca.data.timeframe import TimeFrame

from ..broker_clients.data_client import DataClient
from ....models.logger import Logger

logger = Logger.logger

class AlpacaHistoricalDataClient(DataClient):
    def __init__(self, 
                 api_key: str, 
                 secret_key: str, 
                 symbols: List[str],
                 timeframe: TimeFrame):
        super().__init__(symbols=symbols, timeframe=timeframe)
        self.create_historical_data_client(api_key=api_key,
                                           secret_key=secret_key
                                           )
        

    def create_historical_data_client(self, api_key: str, secret_key: str):
        self.crypto_historical_data_client = CryptoHistoricalDataClient(
                                api_key=api_key,
                                secret_key=secret_key,
                            )
        self.stock_historical_data_client = StockHistoricalDataClient(
                                api_key=api_key,
                                secret_key=secret_key
                            )
        logger.info("Historical Data Client successfully created.")

    def load_warmup(self, lookback: int) -> Dict[str, List[Bar]]:
        # FIXME: Do not assume all the symbols are crypto
        barset = self.crypto_historical_data_client.get_crypto_bars(
                                CryptoBarsRequest(
                                    symbol_or_symbols=self.symbols,
                                    timeframe=self.timeframe,
                                    limit=lookback
                                )
                            )
        
        if isinstance(barset, BarSet):
            warmup = barset.data
        else:
            warmup = barset

        return warmup
    
    def get_latest(self) -> Dict[str, Bar]:
        # FIXME: Do not assume all the symbols are crypto
        latest = self.crypto_historical_data_client.get_crypto_latest_bar(
                                        CryptoLatestBarRequest(
                                            symbol_or_symbols=self.symbols
                                        )
                                    )
        return latest
