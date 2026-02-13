from supabase import create_client, Client
from functools import lru_cache
from config import get_settings


@lru_cache()
def get_supabase_client() -> Client:
    """
    Cria e retorna um cliente Supabase (cached)
    """
    settings = get_settings()
    supabase: Client = create_client(settings.supabase_url, settings.supabase_key)
    return supabase
