import logging

from .config import load_config
from .engine.engine_manager import EngineManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    config = load_config("config.yaml")

    broker_name = config["execution"]["broker"]
    timeframe = config["execution"]["timeframe"]
    strategy_name = config["strategy"]["name"]
    strategy_parameters = config["strategy"]["parameters"]
    symbols = config["strategy"]["symbols"]

    engine_manager = EngineManager(broker_name=broker_name,
                                   timeframe=timeframe,
                                   strategy_name=strategy_name,
                                   strategy_parameters=strategy_parameters,
                                   symbols=symbols,
                                  )

    engine_manager.run()