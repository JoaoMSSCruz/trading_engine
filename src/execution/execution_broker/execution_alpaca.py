from typing import cast, List

from ...common.common import InternalSide
from .execution_broker import ExecutionBroker
from ...models.logger import Logger
from ...models.order import Order
from ...models.position import Position

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
from alpaca.trading.models import Position as BrokerPosition, TradeAccount
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

    def get_positions(self) -> List[Position]:
        broker_positions = self.trading_client.get_all_positions()

        broker_positions= cast(List[BrokerPosition], broker_positions)

        internal_positions = self.broker_positions_to_internal_positions(broker_positions=broker_positions)
        
        return internal_positions

    def get_cash(self) -> float:
        account = self.trading_client.get_account()

        account = cast(TradeAccount, account)

        cash = float(account.cash or 0.0)

        return cash

    def submit_orders(self, internal_orders: List[Order]) -> None:
        alpaca_orders = self.internal_orders_to_broker_orders(internal_orders=internal_orders)

        for alpaca_order in alpaca_orders:
            self.trading_client.submit_order(alpaca_order)

    def internal_orders_to_broker_orders(self, internal_orders: List[Order]) -> List[OrderRequest]:
        alpaca_orders = list()

        for internal_order in internal_orders:
            internal_side = internal_order.get_side()
            alpaca_order = OrderRequest(symbol=internal_order.get_symbol(),
                                        notional=internal_order.get_notional(),
                                        side=self._SIDE_MAPPER[internal_side],
                                        type=OrderType.MARKET, #FIXME: Make this not hardcoded
                                        time_in_force=TimeInForce.GTC #FIXME: Make this not hardcoded
                                        )
            alpaca_orders.append(alpaca_order)

        return alpaca_orders
    
    def broker_positions_to_internal_positions(self, 
                                               broker_positions: List[BrokerPosition]
                                               ) -> List[Position]:
        internal_positions = list()

        for broker_position in broker_positions:
            internal_position = Position(uid=str(broker_position.asset_id),
                                         symbol=broker_position.symbol,
                                         quantity=float(broker_position.qty))
            internal_positions.append(internal_position)
        return internal_positions