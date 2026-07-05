from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class EngineSettings(BaseSettings):
    # System will demand this variables are in the env file
    alpaca_api_key: str
    alpaca_secret_key: SecretStr 

    # Configuration for the pydantic read the env file directly
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = EngineSettings()