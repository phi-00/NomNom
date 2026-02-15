from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from database import get_supabase_client
from pydantic import BaseModel

router = APIRouter()


class ListaComprasItem(BaseModel):
    """Schema para item da lista de compras"""
    idIngrediente: int
    cantidad: int = 1


class ListaComprasResponse(BaseModel):
    """Response de item da lista de compras"""
    idIngrediente: int
    idUtilizador: str
    quantidade: int


@router.get("/usuario/{user_email}")
async def get_lista_compras(user_email: str):
    """
    Retorna todos os itens da lista de compras de um usuário
    
    Parâmetros:
        - user_email: Email do usuário (idUtilizador)
    
    Retorna:
        Lista de itens com detalhes do ingrediente
    """
    try:
        supabase = get_supabase_client()
        
        # Buscar itens da lista de compras com join do ingrediente
        response = supabase.table("ListaCompras").select(
            "idIngrediente, idUtilizador, quantidade, Ingrediente(id, nome, grupo_alimentar, unidade_medida, calorias)"
        ).eq("idUtilizador", user_email).execute()
        
        items = []
        for item in response.data:
            if item.get('Ingrediente'):
                items.append({
                    "idIngrediente": item["idIngrediente"],
                    "idUtilizador": item["idUtilizador"],
                    "quantidade": item["quantidade"],
                    "ingrediente": {
                        "id": item["Ingrediente"]["id"],
                        "nome": item["Ingrediente"]["nome"],
                        "grupo_alimentar": item["Ingrediente"]["grupo_alimentar"],
                        "unidade_medida": item["Ingrediente"]["unidade_medida"],
                        "calorias": item["Ingrediente"]["calorias"]
                    }
                })
        
        return items
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar lista de compras: {str(e)}"
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_to_lista_compras(
    idIngrediente: int,
    idUtilizador: str,
    quantidade: int = 1
):
    """
    Adiciona um item à lista de compras do usuário
    
    Parâmetros:
        - idIngrediente: ID do ingrediente
        - idUtilizador: Email do usuário
        - quantidade: Quantidade (padrão: 1)
    
    Retorna:
        Item adicionado
    """
    try:
        supabase = get_supabase_client()
        
        # Verificar se o item já existe na lista de compras
        existing = supabase.table("ListaCompras").select("*").eq(
            "idIngrediente", idIngrediente
        ).eq("idUtilizador", idUtilizador).execute()
        
        if existing.data and len(existing.data) > 0:
            # Se já existe, apenas atualiza a quantidade
            update_response = supabase.table("ListaCompras").update({
                "quantidade": existing.data[0]["quantidade"] + quantidade
            }).eq("idIngrediente", idIngrediente).eq(
                "idUtilizador", idUtilizador
            ).execute()
            
            if not update_response.data or len(update_response.data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao atualizar item da lista de compras"
                )
            
            return {
                "message": "Item quantity updated",
                "idIngrediente": idIngrediente,
                "idUtilizador": idUtilizador,
                "quantidade": update_response.data[0]["quantidade"]
            }
        
        # Se não existe, cria novo item
        insert_response = supabase.table("ListaCompras").insert({
            "idIngrediente": idIngrediente,
            "idUtilizador": idUtilizador,
            "quantidade": quantidade
        }).execute()
        
        if not insert_response.data or len(insert_response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao adicionar item à lista de compras"
            )
        
        return {
            "message": "Item added to shopping list",
            "idIngrediente": idIngrediente,
            "idUtilizador": idUtilizador,
            "quantidade": quantidade
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao adicionar à lista de compras: {str(e)}"
        )


@router.delete("/item/{id_ingrediente}/{user_email}", status_code=status.HTTP_200_OK)
async def remove_from_lista_compras(id_ingrediente: int, user_email: str):
    """
    Remove um item da lista de compras
    
    Parâmetros:
        - id_ingrediente: ID do ingrediente
        - user_email: Email do usuário
    
    Retorna:
        Confirmação de remoção
    """
    try:
        supabase = get_supabase_client()
        
        # Delete do item
        response = supabase.table("ListaCompras").delete().eq(
            "idIngrediente", id_ingrediente
        ).eq("idUtilizador", user_email).execute()
        
        return {
            "message": "Item removed from shopping list",
            "idIngrediente": id_ingrediente,
            "idUtilizador": user_email
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover da lista de compras: {str(e)}"
        )


@router.delete("/usuario/{user_email}", status_code=status.HTTP_200_OK)
async def clear_lista_compras(user_email: str):
    """
    Limpa toda a lista de compras de um usuário
    
    Parâmetros:
        - user_email: Email do usuário
    
    Retorna:
        Confirmação de limpeza
    """
    try:
        supabase = get_supabase_client()
        
        # Delete de todos os itens do usuário
        response = supabase.table("ListaCompras").delete().eq(
            "idUtilizador", user_email
        ).execute()
        
        return {
            "message": "Shopping list cleared",
            "idUtilizador": user_email
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao limpar lista de compras: {str(e)}"
        )
