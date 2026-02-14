from fastapi import APIRouter, HTTPException, status
from typing import List
from models import Item, ItemCreate, ItemUpdate
from database import get_supabase_client

router = APIRouter()
supabase = get_supabase_client()


@router.get("/items", response_model=List[Item])
async def get_items():
    """
    Retorna todos os itens
    
    Este é um exemplo - ajuste o nome da tabela conforme seu banco
    """
    try:
        response = supabase.table("items").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar itens: {str(e)}"
        )


@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """
    Retorna um item específico por ID
    """
    try:
        response = supabase.table("items").select("*").eq("id", item_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item {item_id} não encontrado"
            )
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar item: {str(e)}"
        )


@router.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    """
    Cria um novo item
    """
    try:
        response = supabase.table("items").insert(item.model_dump()).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar item: {str(e)}"
        )


@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate):
    """
    Atualiza um item existente
    """
    try:
        # Verificar se existe
        existing = supabase.table("items").select("*").eq("id", item_id).execute()
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item {item_id} não encontrado"
            )
        
        # Atualizar apenas campos não-nulos
        update_data = item.model_dump(exclude_unset=True)
        response = supabase.table("items").update(update_data).eq("id", item_id).execute()
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar item: {str(e)}"
        )


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """
    Deleta um item
    """
    try:
        # Verificar se existe
        existing = supabase.table("items").select("*").eq("id", item_id).execute()
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item {item_id} não encontrado"
            )
        
        supabase.table("items").delete().eq("id", item_id).execute()
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar item: {str(e)}"
        )
