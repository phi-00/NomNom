from supabase import create_client, Client
from functools import lru_cache
from src.config import get_settings


@lru_cache()
def get_supabase_client() -> Client:
    """Retorna o cliente do Supabase (cached)"""
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_key)


def get_db() -> Client:
    """Retorna o cliente do Supabase para uso em rotas"""
    return get_supabase_client()