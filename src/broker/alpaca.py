import logging
from typing import cast, List

from alpaca.trading.client import TradingClient
from alpaca.trading.models import Position as External_position

from models.position import Position

from .broker import Broker

logger = logging.getLogger(__name__)

class Alpaca(Broker):
    def __init__(self, api_key: str, secret_key: str):
        self.trading_client = TradingClient(
                                api_key=api_key,
                                secret_key=secret_key,
                            )

        logger.warning("Alpaca TradingClient initialized with paper money.")

    def get_open_positions(self) -> List[Position]: 
        raw_response = self.trading_client.get_all_positions()

        external_positions = cast(List[External_position], raw_response)
        
        return self.normalize_positions(external_positions)

    def get_asset_price(self, asset_name: str):
        pass

    def send_order(self):
        pass

    def normalize_positions(self, external_positions: List[External_position]) -> List[Position]:
        normalized_positions = list()

        for external_position in external_positions:
            position = Position(
                str(external_position.asset_id),
                int(external_position.qty)
            )
            normalized_positions.append(position)
        
        return normalized_positions