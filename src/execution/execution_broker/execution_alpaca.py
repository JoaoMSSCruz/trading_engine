from typing import List


from ...common import InternalSide
from .execution_broker import ExecutionBroker
from ...models.logger import Logger
from ...models.order import Order

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
from alpaca.trading.requests import OrderRequest

logger = Logger.logger

class ExecutionAlpaca(ExecutionBroker):
    _SIDE_MAPPER = {
        InternalSide.BUY: OrderSide.BUY,
        InternalSide.SELL: OrderSide.SELL
    }

    def __init__(self, api_key: str, secret_key: str):
        self.trading_client = TradingClient(
                                api_key=api_key,
                                secret_key=secret_key,
                                paper=True
                            )

        logger.info("Alpaca Execution Broker initialized with paper money.")

    def submit_orders(self, internal_orders: List[Order]) -> None:
        alpaca_orders = self.internal_orders_to_broker_orders(internal_orders=internal_orders)

        """FIXME: Commenting for now so the engine doesn't trade 
        for alpaca_order in alpaca_orders:
            self.trading_client.submit_order(alpaca_order)
        """

    def internal_orders_to_broker_orders(self, internal_orders: List[Order]) -> List[OrderRequest]:
        alpaca_orders = list()

        for internal_order in internal_orders:
            internal_side = internal_order.get_side()
            alpaca_order = OrderRequest(symbol=internal_order.get_symbol(),
                                        qty=internal_order.get_quantity(),
                                        side=self._SIDE_MAPPER[internal_side],
                                        type=OrderType.MARKET, #FIXME: Make this not hardcoded
                                        time_in_force=TimeInForce.GTC #FIXME: Make this not hardcoded
                                        )
            alpaca_orders.append(alpaca_order)

        return alpaca_orders