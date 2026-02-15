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


@router.get("/test-inventario")
async def test_inventario_table():
    """
    Testa a tabela Inventário para verificar estrutura e RLS
    """
    supabase = get_supabase_client()
    results = {}
    
    try:
        # Test 1: Try to select all from Inventário
        response = supabase.table("Inventário").select("*").execute()
        results["select_all"] = {
            "success": True,
            "count": len(response.data) if response.data else 0,
            "sample": response.data[:3] if response.data else []
        }
    except Exception as e:
        results["select_all"] = {
            "success": False,
            "error": str(e)
        }
    
    try:
        # Test 2: Try to get columns from a single record
        response = supabase.table("Inventário").select("*").limit(1).execute()
        if response.data and len(response.data) > 0:
            results["columns"] = list(response.data[0].keys())
        else:
            results["columns"] = "No data to extract columns from"
    except Exception as e:
        results["columns_error"] = str(e)
    
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


@router.post("")
async def create_ingrediente(ingredient_data: Dict[str, Any]):
    """
    Cria um novo ingrediente na base de dados
    
    Params:
        - nome: nome do ingrediente
        - grupo_alimentar: grupo alimentar (frutas, ovos, etc.)
        - unidade_medida: unidade de medida (g, ml, un, etc.)
        - calorias: calorias por unidade de medida
    """
    try:
        supabase = get_supabase_client()
        
        nome = ingredient_data.get("nome")
        grupo_alimentar = ingredient_data.get("grupo_alimentar")
        unidade_medida = ingredient_data.get("unidade_medida", "g")
        calorias = ingredient_data.get("calorias", 0)
        
        if not nome or not grupo_alimentar:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="nome e grupo_alimentar são obrigatórios"
            )
        
        # Insert new ingredient
        response = supabase.table("Ingrediente").insert({
            "nome": nome,
            "grupo_alimentar": grupo_alimentar,
            "unidade_medida": unidade_medida,
            "calorias": calorias
        }).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar ingrediente"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar ingrediente: {str(e)}"
        )

@router.get("/inventario/{user_email}")
async def get_user_inventory(user_email: str):
    """
    Retorna o inventário de ingredientes de um usuário específico
    Busca na tabela Inventario e faz JOIN com Ingrediente para obter detalhes completos
    """
    try:
        supabase = get_supabase_client()
        
        response = supabase.table("Inventário").select(
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


@router.post("/inventario")
async def add_to_inventory(inventory_item: Dict[str, Any]):
    """
    Adiciona ou atualiza um ingrediente no inventário do utilizador
    
    Params:
        - idUtilizador: email do utilizador
        - idIngrediente: ID do ingrediente
        - quantidade: quantidade a adicionar
    """
    try:
        supabase = get_supabase_client()
        
        id_utilizador = inventory_item.get("idUtilizador")
        id_ingrediente = inventory_item.get("idIngrediente")
        quantidade = inventory_item.get("quantidade", 1)
        
        if not id_utilizador or not id_ingrediente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="idUtilizador e idIngrediente são obrigatórios"
            )
        
        # Check if item already exists in inventory
        existing = supabase.table("Inventário").select("*").eq(
            "idUtilizador", id_utilizador
        ).eq("idIngrediente", id_ingrediente).execute()
        
        if existing.data and len(existing.data) > 0:
            # Update existing quantity
            new_quantity = existing.data[0]["quantidade"] + quantidade
            response = supabase.table("Inventário").update({
                "quantidade": new_quantity
            }).eq("idUtilizador", id_utilizador).eq(
                "idIngrediente", id_ingrediente
            ).execute()
        else:
            # Insert new item
            response = supabase.table("Inventário").insert({
                "idUtilizador": id_utilizador,
                "idIngrediente": id_ingrediente,
                "quantidade": quantidade
            }).execute()
                
        return {
            "message": "Item adicionado ao inventário com sucesso",
            "data": response.data if hasattr(response, 'data') else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao adicionar item ao inventário: {str(e)}"
        )


@router.patch("/inventario")
async def update_inventory_quantity(inventory_update: Dict[str, Any]):
    """
    Atualiza a quantidade de um ingrediente no inventário do utilizador
    
    Params:
        - idUtilizador: email do utilizador
        - idIngrediente: ID do ingrediente
        - quantidade: nova quantidade (substitui a quantidade existente)
    """
    try:
        supabase = get_supabase_client()
        
        id_utilizador = inventory_update.get("idUtilizador")
        id_ingrediente = inventory_update.get("idIngrediente")
        quantidade = inventory_update.get("quantidade")
        
        if not id_utilizador or not id_ingrediente or quantidade is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="idUtilizador, idIngrediente e quantidade são obrigatórios"
            )
        
        # Update the quantity
        response = supabase.table("Inventário").update({
            "quantidade": quantidade
        }).eq("idUtilizador", id_utilizador).eq(
            "idIngrediente", id_ingrediente
        ).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item não encontrado no inventário"
            )
        
        return {
            "message": "Quantidade atualizada com sucesso",
            "data": response.data[0] if response.data else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar quantidade: {str(e)}"
        )


@router.delete("/inventario")
async def remove_from_inventory(inventory_item: Dict[str, Any]):
    """
    Remove um ingrediente do inventário do utilizador
    
    Params:
        - idUtilizador: email do utilizador
        - idIngrediente: ID do ingrediente
    """
    try:
        supabase = get_supabase_client()
        
        id_utilizador = inventory_item.get("idUtilizador")
        id_ingrediente = inventory_item.get("idIngrediente")
        
        if not id_utilizador or not id_ingrediente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="idUtilizador e idIngrediente são obrigatórios"
            )
        
        # Delete the item from inventory
        response = supabase.table("Inventário").delete().eq(
            "idUtilizador", id_utilizador
        ).eq("idIngrediente", id_ingrediente).execute()
        
        return {
            "message": "Item removido do inventário com sucesso",
            "data": response.data if hasattr(response, 'data') else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover item do inventário: {str(e)}"
        )
