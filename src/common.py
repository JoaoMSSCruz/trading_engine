from enum import Enum
from alpaca.trading.enums import OrderSide

class alpaca_side(Enum):
    BUY = OrderSide.BUY
    SELL = OrderSide.SELL
