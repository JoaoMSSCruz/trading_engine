from typing import Dict, List

from alpaca.data.live import CryptoDataStream, StockDataStream
from alpaca.data.models.bars import Bar as AlpacaBar
from alpaca.data.timeframe import TimeFrame

from ..broker_clients.data_client import DataClient
from ....models.logger import Logger

logger = Logger.logger

class AlpacaDataStreamClient(DataClient):
    def __init__(self, 
                     api_key: str, 
                     secret_key: str, 
                     symbols: List[str],
                     timeframe: TimeFrame):
            super().__init__(symbols=symbols, timeframe=timeframe)
            self.create_data_stream_client(api_key=api_key,
                                               secret_key=secret_key
                                               )

    def create_data_stream_client(self, api_key: str, secret_key: str):
        self.crypto_historical_data_client = CryptoDataStream(
                                        api_key=api_key,
                                        secret_key=secret_key,
                                    )
        
        self.stock_historical_data_client = StockDataStream(
                                        api_key=api_key,
                                        secret_key=secret_key
                                    )

        # FIXME: Refactor this for better architecture
        self.subscribe()
        logger.info("Data Streams successfully created.")

    def subscribe(self):
         self.crypto_historical_data_client.subscribe_bars(handler=self.on_receive,
                                                           *self.symbols
                                                           ) 

         self.crypto_historical_data_client.run()  

    async def on_receive(self, bar: AlpacaBar | Dict) -> None:    
        logger.info(bar)
        