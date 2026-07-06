import logging

from .broker.alpaca import Alpaca
from .config import settings

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    alpaca_broker = Alpaca( 
        settings.alpaca_api_key, 
        settings.alpaca_secret_key.get_secret_value()
        )
