from abc import ABC, abstractmethod

class Broker(ABC):
    @abstractmethod
    def get_portfolio_state(self):
        pass

    @abstractmethod
    def get_asset_price(self, asset_name: str):
        '''TODO: Define a way to inform the interval of time
                A good way would be to have a timeframe and a quantity''' 
        pass

    @abstractmethod
    def send_order(self):
        '''TODO: Use interal class that represent an order
                Have an Order as a parameter''' 
        pass