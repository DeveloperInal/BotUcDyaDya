from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    token: str = Field(alias='TOKEN')
    http_client: str = Field(alias='HTTP_CLIENT')
    
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='forbid'
    )
    
settings = Settings()    