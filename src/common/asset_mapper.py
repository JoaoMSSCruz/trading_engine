"""This is a mapper from a general asset name, to the broker names per se"""
import json
from pathlib import Path
from typing import Dict

class AssetMapper:
    def __init__(self, assets: Dict[str, Dict[str, str]]):
        self.assets = assets

        """A reverse map is very useful for O(1) search"""
        self._reverse_map = {
            (broker_name, broker_symbol): internal_symbol
            for internal_symbol, broker_mappings in self.assets.items()
            for broker_name, broker_symbol in broker_mappings.items()
        }

    @classmethod
    def from_json(cls, file_path: str) -> 'AssetMapper':
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File {file_path} not found.")
            
        with open(path, 'r') as file:
            config = json.load(file)
            
        return cls(config)

    def get_broker_symbol(self, internal_asset: str, broker_name: str) -> str:
        if internal_asset not in self.assets:
            raise ValueError(f"Asset {internal_asset} not present in the engine.")
        if broker_name not in self.assets[internal_asset]:
            raise ValueError(f"Asset {internal_asset} not present in {broker_name} assets.")
        return self.assets[internal_asset][broker_name]

    def get_internal_asset(self, broker_name: str, symbol: str) -> str:
        if (broker_name, symbol) not in self._reverse_map:
            raise ValueError(f"Pair Broker: {broker_name}, Symbol: {symbol} not present.")
        return self._reverse_map[(broker_name, symbol)]
        