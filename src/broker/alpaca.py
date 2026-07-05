import logging

from alpaca.trading.client import TradingClient

from .broker import Broker

logger = logging.getLogger(__name__)

class Alpaca(Broker):
    def __init__(self, api_key: str, secret_key: str):
        self.trading_client = TradingClient(
                                api_key=api_key,
                                secret_key=secret_key,
                            )

        logger.warning("Alpaca TradingClient initialized with paper money.")

    def get_portfolio_state(self): 
        pass

    def get_asset_price(self, asset_name: str):
        pass

    def send_order(self):
        pass