from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings
from config import TOKEN, HTTP_SERVER

class ServerConfig(BaseModel):
    http_server: str = HTTP_SERVER

class Settings(BaseSettings):
    token: str = TOKEN
    server: ServerConfig = ServerConfig()
    
    model_config = ConfigDict(extra='forbid')
    
settings = Settings()    