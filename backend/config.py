from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Supabase
    supabase_url: str
    supabase_key: str
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Retorna as configurações da aplicação (cached)"""
    return Settings()
