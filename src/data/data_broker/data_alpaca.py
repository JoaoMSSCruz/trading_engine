from typing import List, Dict

from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.live import CryptoDataStream, StockDataStream
from alpaca.data.models import BarSet
from alpaca.data.models.bars import Bar as Alpaca_bar
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

from ...common import InternalTimeframe
from .data_broker import DataBroker
from ...models.bar import Bar
from ...models.logger import Logger

logger = Logger.logger

class DataAlpaca(DataBroker):
    _TIMEFRAME_MAPPER = {
        InternalTimeframe.MINUTE: TimeFrame.Minute,
        InternalTimeframe.HOUR: TimeFrame.Hour,
        InternalTimeframe.DAY: TimeFrame.Day,
        InternalTimeframe.WEEK: TimeFrame.Week,
        InternalTimeframe.MONTH: TimeFrame.Month,
    }

    def __init__(self, api_key: str, secret_key: str):
        self.crypto_historical_data_client = CryptoHistoricalDataClient(
                                api_key=api_key,
                                secret_key=secret_key,
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

    def create_data_stream_client(self, api_key: str, secret_key: str):
        self.crypto_data_stream_client = CryptoDataStream(
                                api_key=api_key,
                                secret_key=secret_key
                            ) 
        self.stock_data_stream_client = StockDataStream(
                                api_key=api_key,
                                secret_key=secret_key
                            ) 
        
        logger.info("Stream Data Client successfully created.")

    def connect_data_stream(self):
        # FIXME: Find a way to connect only the necessary streams
        self.crypto_data_stream_client.run()
        self.stock_data_stream_client.run()

        logger.info("Data Streams connected.")

    def desconnect_data_stream(self):
        # FIXME: Desconnect only the active streams
        self.crypto_data_stream_client.stop()
        self.stock_data_stream_client.stop()

        logger.info("Data Streams desocnnected.")

    def get_assets_bars(self, 
                        symbols: List[str],
                        internal_timeframe: InternalTimeframe,
                        limit: int
                        ) -> Dict[str, List[Bar]]:
        """FIXME: For now we can only trade crypto, but stocks and commodities must be traded as well"""

        internal_bars = dict()
        alpaca_timeframe = self._TIMEFRAME_MAPPER[internal_timeframe]

        alpaca_barset = self.crypto_historical_data_client.get_crypto_bars(
                                CryptoBarsRequest(
                                    symbol_or_symbols=symbols,
                                    timeframe=alpaca_timeframe,
                                    limit=limit
                                )

                            )
        
        if isinstance(alpaca_barset, BarSet):
            alpaca_bars_dict = alpaca_barset.data
        else:
            alpaca_bars_dict = alpaca_barset

        for symbol in symbols:
            if symbol in alpaca_bars_dict.keys():
                internal_bars[symbol] = self.broker_bars_to_internal_bars(alpaca_bars=alpaca_bars_dict[symbol])

        return internal_bars
    
    @staticmethod
    def broker_bars_to_internal_bars(alpaca_bars: List[Alpaca_bar]) -> List[Bar]:
        internal_bars = list()

        for alpaca_bar in alpaca_bars:
            internal_bar = Bar(
                            symbol=alpaca_bar.symbol,
                            timestamp=alpaca_bar.timestamp,\
                            open=alpaca_bar.open,
                            high=alpaca_bar.high,
                            low=alpaca_bar.low,
                            close=alpaca_bar.close,
                            volume=alpaca_bar.volume
                        )
            internal_bars.append(internal_bar)

        return internal_bars
        