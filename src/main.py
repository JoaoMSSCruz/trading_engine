# TODO-39: Have the Database connection done elsewhere. Perhaps in the DataManager

from .common.asset_mapper import AssetMapper 
from data.database.connection import DatabaseManager
from .config import load_config
from .engine.engine_manager import EngineManager
from data.database.repository import MarketDataRepository
import os

if __name__ == "__main__":
    asset_mapper = AssetMapper.from_json("assets.json")

    # FIXME-39: The whole DB handling is only temporary
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    db_name = os.environ["POSTGRES_DB"]

    DB_URL = f"postgresql://{user}:{password}@postgres-db:5432/{db_name}"

    db_manager = DatabaseManager(DB_URL)
    db_manager.connect()

    db_repository = MarketDataRepository(db_manager)

    config = load_config("config.yaml")

    data_broker_name = config["data"]["broker"]
    data_timeframe = config["data"]["timeframe"]
    strategy_name = config["strategy"]["name"]
    strategy_lookback = config["strategy"]["lookback"]
    strategy_parameters = config["strategy"]["parameters"]
    symbols = config["strategy"]["symbols"]
    execution_broker_name = config["execution"]["broker"]


    asset_mapper = AssetMapper.from_json("assets.json")

    engine_manager = EngineManager(
                        asset_mapper=asset_mapper,
                        data_broker_name=data_broker_name,
                        data_timeframe=data_timeframe,
                        strategy_name=strategy_name,
                        strategy_lookback=strategy_lookback,
                        strategy_parameters=strategy_parameters,
                        symbols=symbols,
                        execution_broker_name=execution_broker_name,
                    )

    engine_manager.start_engine()