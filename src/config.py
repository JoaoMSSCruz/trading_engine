import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from typing import Any, Dict
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(file_path: str = "config.yaml") -> Dict[str, Any]:
    try:
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
        
        logger.info(f"Config successfully loaded: {file_path}")
        return config
        
    except FileNotFoundError:
        logger.critical(f"Config file not founded: {file_path}")
        raise
    except yaml.YAMLError as exc:
        logger.critical(f"Syntax error in yaml file: {exc}")
        raise

class EngineSettings(BaseSettings):
    # System will demand this variables are in the env file
    api_key: str
    secret_key: SecretStr 

    # Configuration for the pydantic read the env file directly
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = EngineSettings() # type: ignore (to ignore the error message, since it is only recognized in runtime)