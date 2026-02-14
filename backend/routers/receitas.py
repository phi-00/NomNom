from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from database import get_supabase_client

router = APIRouter()


@router.get("/test-tables")
async def test_receitas_table():
    """
    Testa se a tabela Receita existe e retorna informações sobre ela
    """
    supabase = get_supabase_client()
    results = {}
    
    try:
        # Teste 1: Select normal
        response1 = supabase.table("Receita").select("*").execute()
        
        # Teste 2: Select com count
        response2 = supabase.table("Receita").select("*", count="exact").execute()
        
        results["Receita"] = {
            "select_all": {
                "success": True,
                "data_count": len(response1.data) if response1.data else 0,
                "has_data": bool(response1.data),
                "sample_data": response1.data[:2] if response1.data else []
            },
            "with_count": {
                "count": response2.count if hasattr(response2, 'count') else "N/A",
                "data_count": len(response2.data) if response2.data else 0
            }
        }
    except Exception as e:
        results["Receita"] = {
            "success": False,
            "error": str(e)
        }
    
    return results


@router.get("")
async def get_receitas():
    """
    Retorna todas as receitas com suas informações completas
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("Receita").select("*").execute()
        return response.data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar receitas: {str(e)}"
        )


@router.get("/minhas")
async def get_minhas_receitas(user_email: str = None):
    """
    Retorna receitas do usuário (minhas receitas)
    Se user_email for fornecido, filtra por esse usuário
    """
    try:
        supabase = get_supabase_client()
        
        # Se houver user_email, filtrar por usuário
        if user_email:
            response = supabase.table("Receita").select("*").eq("user_email", user_email).execute()
        else:
            # Caso contrário, retornar todas com type="my"
            response = supabase.table("Receita").select("*").execute()
            # Filtrar apenas as marcadas como "my" se o campo existir
            data = response.data or []
            data = [r for r in data if r.get("tipo") == "minha" or r.get("type") == "my"]
            return data if data else response.data  # Se nenhuma com tipo, retorna tudo
        
        return response.data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar minhas receitas: {str(e)}"
        )


@router.get("/outras")
async def get_outras_receitas():
    """
    Retorna outras receitas (receitas de outros usuários)
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("Receita").select("*").execute()
        
        # Se houver campo tipo/type, filtrar por outras
        data = response.data or []
        data_com_tipo = [r for r in data if r.get("tipo") == "outra" or r.get("type") == "other"]
        
        # Se não houver com tipo específico, retornar tudo
        return data_com_tipo if data_com_tipo else data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar outras receitas: {str(e)}"
        )
