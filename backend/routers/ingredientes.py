from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from database import get_supabase_client
import json

router = APIRouter()


@router.get("/test-tables")
async def test_table_names():
    """
    Testa diferentes variações do nome da tabela e verifica RLS
    """
    supabase = get_supabase_client()
    results = {}
    
    # Testar com a tabela correta
    try:
        # Teste 1: Select normal
        response1 = supabase.table("Ingrediente").select("*").execute()
        
        # Teste 2: Select com count
        response2 = supabase.table("Ingrediente").select("*", count="exact").execute()
        
        results["Ingrediente"] = {
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
        results["Ingrediente"] = {
            "success": False,
            "error": str(e)
        }
    
    return results


@router.get("/columns")
async def get_ingredientes_columns():
    """
    Retorna os nomes de todas as colunas da tabela Ingrediente
    
    Returns:
        List[Dict]: Lista com o nome de cada coluna
            Exemplo: [{"column_name": "id"}, {"column_name": "nome"}, ...]
    """
    try:
        supabase = get_supabase_client()
        
        # Tentar buscar ao menos um registro para obter as colunas
        response = supabase.table("Ingrediente").select("*").limit(1).execute()
        
        # Se houver dados, extrair colunas
        if response.data and len(response.data) > 0:
            columns = list(response.data[0].keys())
            return {
                "table": "Ingrediente",
                "columns": [{"column_name": col} for col in columns],
                "total_columns": len(columns)
            }
        
        # Se a tabela estiver vazia, retornar erro mais claro
        return {
            "table": "Ingrediente",
            "columns": [],
            "total_columns": 0,
            "message": "A tabela existe mas está vazia. Adicione dados para ver as colunas."
        }
        
    except Exception as e:
        # Capturar o erro e retornar detalhes
        error_detail = str(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail
        )


@router.get("/preview")
async def get_ingredientes_preview():
    """
    Retorna um preview da tabela Ingrediente (primeiros registros)
    com informações sobre as colunas
    """
    try:
        supabase = get_supabase_client()
        
        # Buscar primeiros registros
        response = supabase.table("Ingrediente").select("*").limit(10).execute()
        
        columns = []
        if response.data:
            columns = list(response.data[0].keys())
        
        return {
            "table": "Ingrediente",
            "columns": [{"column_name": col} for col in columns],
            "total_columns": len(columns),
            "data": response.data,
            "total_records": len(response.data)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar preview da tabela Ingrediente: {str(e)}"
        )


@router.get("")
async def get_ingredientes():
    """
    Retorna todos os ingredientes com suas informações completas
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("Ingrediente").select("*").execute()
        return response.data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar ingredientes: {str(e)}"
        )

@router.get("/inventario/{user_email}")
async def get_user_inventory(user_email: str):
    """
    Retorna o inventário de ingredientes de um usuário específico
    Busca na tabela Inventario e faz JOIN com Ingrediente para obter detalhes completos
    """
    try:
        supabase = get_supabase_client()
        
        response = supabase.table("Inventario").select(
            "idIngrediente, idUtilizador, quantidade, Ingrediente(id, nome, grupo_alimentar, unidade_medida, calorias)"
        ).eq("idUtilizador", user_email).execute()
        
        inventory = []
        for item in response.data:
            if item.get('Ingrediente'):
                inventory.append({
                    "idIngrediente": item["idIngrediente"],
                    "quantidade": item["quantidade"],
                    "id": item["Ingrediente"]["id"],
                    "nome": item["Ingrediente"]["nome"],
                    "grupo_alimentar": item["Ingrediente"]["grupo_alimentar"],
                    "unidade_medida": item["Ingrediente"]["unidade_medida"],
                    "calorias": item["Ingrediente"]["calorias"]
                })
        
        return inventory
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao abrir frigorífico: {str(e)}"
        )
