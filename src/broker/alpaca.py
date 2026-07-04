from .broker import Broker

class Alpaca(Broker):
    def __init__(self):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass

    def get_portfolio_state(self):
        pass

    def get_asset_price(self, asset_name: str):
        pass

    def send_order(self):
        pass