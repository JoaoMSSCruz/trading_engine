from .broker.alpaca import Alpaca
from .config import settings

if __name__ == "__main__":
    # TODO: Make it so that arguments are parsed (api keys, etc) 
    alpaca_broker = Alpaca( 
        settings.alpaca_api_key, 
        settings.alpaca_secret_key.get_secret_value()
        )
        