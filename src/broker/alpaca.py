import logging
from typing import cast, Dict, List

from alpaca.data.models.bars import Bar as Alpaca_bar
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.models import Position as External_position

from ..models.position import Position
from ..models.bar import Bar
from .broker import Broker

logger = logging.getLogger(__name__)

class Alpaca(Broker):
    def __init__(self, api_key: str, secret_key: str):
        self.trading_client = TradingClient(
                                api_key=api_key,
                                secret_key=secret_key,
                            )
        self.stock_historical_data_client = StockHistoricalDataClient(
                                api_key=api_key,
                                secret_key=secret_key,
                            )

        logger.warning("Alpaca TradingClient initialized with paper money.")

    def get_open_positions(self) -> List[Position]: 
        raw_response = self.trading_client.get_all_positions()

        external_positions = cast(List[External_position], raw_response)

        return self.normalize_positions(external_positions)

    def get_asset_bars(self, symbol: str, timeframe: TimeFrame) -> List[Bar]:
        alpaca_bars = self.stock_historical_data_client.get_stock_bars(
                                StockBarsRequest(
                                    symbol_or_symbols=symbol,
                                    timeframe=timeframe
                                )

                            )
        alpaca_bars = cast(Dict[str, List[Alpaca_bar]], alpaca_bars)

        internal_bars = self.alpaca_bars_to_internal_bars(symbol=symbol, alpaca_bars=alpaca_bars)

        return internal_bars

    def send_order(self):
        # FIXME: Implement this
        pass

    def normalize_positions(self, external_positions: List[External_position]) -> List[Position]:
        normalized_positions = list()

        for external_position in external_positions:
            position = Position(
                str(external_position.asset_id),
                str(external_position.symbol),
                int(external_position.qty)
            )
            normalized_positions.append(position)
        
        return normalized_positions
    
    @staticmethod
    def alpaca_bars_to_internal_bars(symbol: str, alpaca_bars: Dict[str, List[Alpaca_bar]]):
        internal_bars = []

        for alpaca_bar in alpaca_bars[symbol]:
            internal_bar = Bar(
                            alpaca_bar.symbol,
                            alpaca_bar.timestamp,
                            alpaca_bar.open,
                            alpaca_bar.high,
                            alpaca_bar.low,
                            alpaca_bar.close,
                            alpaca_bar.volume
                        )
            internal_bars.append(internal_bar)

        return internal_bars