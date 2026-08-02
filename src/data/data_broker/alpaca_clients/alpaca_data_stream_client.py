import asyncio
from typing import Any, cast, Dict, List

from alpaca.data.live import CryptoDataStream, StockDataStream
from alpaca.data.models.bars import Bar as AlpacaBar
from alpaca.data.timeframe import TimeFrame

from ..broker_clients.data_client import DataClient
from ....models.logger import Logger

logger = Logger.logger

"""TODO: Both 1 minute and 1 hour candles (of stocks) will have to be obtained via websocket.
For the 1 hour warmup we won't need it, but for the latest we can't accept the 15 minute delay.
One solution is to subscribe to 1 minute candles and acumulate the information until it reaches
1 hour.
"""

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
        logger.info("Data Streams successfully created.")

    def subscribe(self):
        self.crypto_historical_data_client.subscribe_bars(handler=self.on_receive,
                                                        *self.symbols
                                                        ) 

        self.reset_bar_buffer()

        self.crypto_historical_data_client.run()  

    async def on_receive(self, bar: AlpacaBar | Dict) -> None:   
        bar = cast(AlpacaBar, bar)
         
        self.add_bar_to_buffer(bar=bar)

        if self.reset_timeframe_bars == 0:
            self.first_bar_event.set()

        logger.info(f"Received bar from asset: {bar.symbol}")

    async def load_warmup(self, lookback: int) -> Dict[str, List[AlpacaBar]]:
        self.first_bar_event = asyncio.Event()
        self.subscribe()

        while True:
            await self.first_bar_event.wait()
            
            await asyncio.sleep(5)
            
            if self.timeframe_bars == len(self.symbols):
                logger.info("Received all the bars for the timeframe.")
                
                if self.received_enough_bars(size=lookback):
                    return self.bar_buffer
                
            else:
                logger.warning("Timeout, not all symbols received a bar. Reseting bar buffer...")
                
                self.reset_bar_buffer()
                self.first_bar_event.clear() 

    def get_latest(self) -> Dict[str, Any]:
        #TODO: Implement this
        return {}


    def add_bar_to_buffer(self, bar: AlpacaBar) -> None:
        symbol = bar.symbol

        if symbol not in self.bar_buffer:
            self.bar_buffer[symbol] = list()
        self.bar_buffer[symbol].append(bar)

        self.increment_timeframe_bars()

    def reset_bar_buffer(self):
        self.bar_buffer = dict()

        """This variable counts the ammount of bars received in the timeframe (1 minuto),
        plus a threshold (5 seconds)"""
        self.reset_timeframe_bars()

    def received_enough_bars(self, size: int) -> bool:
        for barset in self.bar_buffer.values():
            if len(barset) != size:
                return False

        return True

    def increment_timeframe_bars(self):
        self.timeframe_bars += 1

    def reset_timeframe_bars(self):
        self.timeframe_bars = 0

        