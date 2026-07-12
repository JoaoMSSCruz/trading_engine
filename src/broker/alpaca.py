import logging
from typing import cast, Dict, List

from alpaca.data.models import BarSet
from alpaca.data.models.bars import Bar as Alpaca_bar
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
from alpaca.trading.models import Position as External_position
from alpaca.trading.requests import OrderRequest

from .broker import Broker
from ..common import InternalSide, InternalTimeframe
from ..models.bar import Bar
from ..models.position import Position
from ..models.order import Order

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Alpaca(Broker):
    """Internal representation of the Alpaca Broker API"""
    _SIDE_MAPPER = {
        InternalSide.BUY: OrderSide.BUY,
        InternalSide.SELL: OrderSide.SELL,
    }
    _TIMEFRAME_MAPPER = {
        InternalTimeframe.MINUTE: TimeFrame.Minute,
        InternalTimeframe.HOUR: TimeFrame.Hour,
        InternalTimeframe.DAY: TimeFrame.Day,
        InternalTimeframe.WEEK: TimeFrame.Week,
        InternalTimeframe.MONTH: TimeFrame.Month,
    }

    def __init__(self, api_key: str, secret_key: str):
        self.trading_client = TradingClient(
                                api_key=api_key,
                                secret_key=secret_key,
                            )
        self.stock_historical_data_client = StockHistoricalDataClient(
                                api_key=api_key,
                                secret_key=secret_key,
                            )

        logger.info("Alpaca Broker initialized with paper money.")

    def get_open_positions(self) -> List[Position]: 
        raw_response = self.trading_client.get_all_positions()

        external_positions = cast(List[External_position], raw_response)

        return self.normalize_positions(external_positions)

    def get_assets_bar(self, symbols: List[str], internal_timeframe: InternalTimeframe) -> Dict[str, List[Bar]]:
        """FIXME: For now we can only trade stocks, but crypto and commodities must be traded as well"""

        internal_bars = dict()
        alpaca_timeframe = self._TIMEFRAME_MAPPER[internal_timeframe]

        alpaca_barset = self.stock_historical_data_client.get_stock_bars(
                                StockBarsRequest(
                                    symbol_or_symbols=symbols,
                                    timeframe=alpaca_timeframe,
                                )

                            )
        
        if isinstance(alpaca_barset, BarSet):
            alpaca_bars_dict = alpaca_barset.data
        else:
            alpaca_bars_dict = alpaca_barset

        for symbol in symbols:
            if symbol in alpaca_bars_dict.keys():
                internal_bars[symbol] = self.alpaca_bars_to_internal_bars(alpaca_bars=alpaca_bars_dict[symbol])

        return internal_bars

    def send_order(self, internal_order: Order) -> None:
        order_request = self.internal_order_to_order_request(
                            internal_order=internal_order, 
                            side_mapper=self._SIDE_MAPPER)
        
        self.trading_client.submit_order(order_request)

    @staticmethod
    def normalize_positions(external_positions: List[External_position]) -> List[Position]:
        normalized_positions = list()
        for external_position in external_positions:
            position = Position(
                str(external_position.asset_id),
                external_position.symbol,
                float(external_position.qty)
            )
            normalized_positions.append(position)
        
        return normalized_positions
    
    @staticmethod
    def alpaca_bars_to_internal_bars(alpaca_bars: List[Alpaca_bar]) -> List[Bar]:
        internal_bars = list()

        for alpaca_bar in alpaca_bars:
            internal_bar = Bar(
                            symbol=alpaca_bar.symbol,
                            timestamp=alpaca_bar.timestamp,
                            open=alpaca_bar.open,
                            high=alpaca_bar.high,
                            low=alpaca_bar.low,
                            close=alpaca_bar.close,
                            volume=alpaca_bar.volume
                        )
            internal_bars.append(internal_bar)

        return internal_bars
    
    @staticmethod
    def internal_order_to_order_request(
        internal_order: Order,
        side_mapper: Dict[InternalSide, OrderSide],
        ) -> OrderRequest:

        """ TODO: Perhaps have the type and time_in_force done dynamically.
            This might not be needed since we will probably only need Day orders.
            However, would be interesting to have them anyway.
        """
        alpaca_side = side_mapper[internal_order.get_side()]

        order_request = OrderRequest(
                            symbol=internal_order.get_symbol(),
                            qty=internal_order.get_quantity(),
                            type=OrderType.MARKET,
                            time_in_force=TimeInForce.DAY,
                            side=alpaca_side
                        )
        
        return order_request