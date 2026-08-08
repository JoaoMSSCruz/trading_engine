import importlib
from typing import Dict, List, Tuple

from ..common.common import InternalSide, InternalTimeframe
from .execution_broker.execution_broker import ExecutionBroker
from .execution_broker.mapper import BROKER_MAPPER
from ..models.bar import Bar
from ..models.logger import Logger
from ..models.order import Order
from ..models.portfolio import Portfolio
from ..models.weights import Weights

logger = Logger.logger

class ExecutionManager:
    def __init__(self, broker_name: str, **parameters):
        self.execution_broker = self.create_broker(broker_name=broker_name,
                                                   **parameters)
        self.portfolio = self.get_portfolio()

    @staticmethod
    def create_broker(broker_name: str, **parameters) -> ExecutionBroker:
        try:
            broker_module_path = BROKER_MAPPER[broker_name]["execution_broker_module_path"]
            broker_class_name = BROKER_MAPPER[broker_name]["execution_broker_class_name"]

            module = importlib.import_module(broker_module_path)

            broker_class = getattr(module, broker_class_name)

            if not issubclass(broker_class, ExecutionBroker):
                raise TypeError(f"Class {broker_class_name} doesn't inherit class Broker.")

            broker = broker_class(**parameters)
            
            return broker
             
        except Exception as e:
            logger.critical(f"Error creating broker: {e}")
            raise

    def get_portfolio(self) -> Portfolio:
        return self.execution_broker.get_portfolio()

    def execute(self, weights: Weights, bars: Dict[str, List[Bar]]) -> None:
        #FIXME: Handle Errors
        self.portfolio = self.get_portfolio()

        portfolio_value = self.calculate_portoflio_value(bars=bars)

        total_value = portfolio_value[0]
        positions_value = portfolio_value[1]

        future_values = self.weights_to_notionals(weights=weights,
                                                  total_value=total_value,
                                                  )
        
        orders = self.convert_deltas_to_orders(positions_value=positions_value,
                                               future_values=future_values,
                                               total_value=total_value
                                               ) 

        self.submit_orders(orders=orders)


    def convert_deltas_to_orders(self, 
                                 positions_value: Dict[str, float], 
                                 future_values: Dict[str, float], 
                                 total_value: float
                                 ) -> List[Order]:
        orders = list()

        threshold = total_value * 0.005 # Let's establish the minimum Order size as 0.5% of Portfolio

        for symbol, future_value in future_values.items():
            current_value = positions_value.get(symbol, 0.0)
            side = InternalSide.BUY
            delta = future_value - current_value

            if delta < 0:
                delta *= -1
                side = InternalSide.SELL

            if delta < threshold:
                continue

            order = Order(symbol=symbol,
                          notional=delta,
                          side=side,
                        )
            orders.append(order)
        return orders


    def weights_to_notionals(self, weights: Weights, total_value: float) -> Dict[str, float]:
        assets_notionals = dict()

        for symbol, weight in weights.get_weights().items():
            assets_notionals[symbol] = weight * total_value

        return assets_notionals

    def submit_orders(self, orders: List[Order]) -> None:
        self.execution_broker.submit_orders(internal_orders=orders)

    """FIXME: Some values, such as the portfolio's value, should be calculate by the Portfolio"""
    def calculate_portoflio_value(self, bars: Dict[str, List[Bar]]) -> Tuple[float, Dict[str, float]]:
        #FIXME: Handle Errors and make it cleaner
        positions_value = dict()
        
        total_value = self.portfolio.get_cash()
        for symbol, bar_objects in bars.items():
            # Get the last known price of the asset
            bar = bar_objects.pop()
            
            position = self.portfolio.get_position(symbol=symbol)
            if position is None:
                positions_value[symbol] = 0.0
                continue
            position_value = bar.get_close() * position.get_quantity()
            
            positions_value[symbol] = position_value

            total_value += position_value

        return (total_value, positions_value)

