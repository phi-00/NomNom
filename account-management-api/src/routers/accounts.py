from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from src.schemas.account import AccountCreate, AccountResponse, AccountUpdate
from src.services.account_service import account_service

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"]
)


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(account_data: AccountCreate):
    """
    Cria uma nova conta de usuário no Supabase
    
    - **name**: Nome do usuário (2-100 caracteres)
    - **email**: Email válido
    - **password**: Senha (mínimo 6 caracteres)
    """
    try:
        account = await account_service.create_account(account_data)
        return account
    except ValueError as e:
        if "já está registrado" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar conta: {str(e)}"
        )


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(account_id: str):
    """
    Busca uma conta por ID (UUID)
    """
    account = await account_service.get_account_by_id(account_id)
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada"
        )
    
    return account


@router.get("/", response_model=List[AccountResponse])
async def list_accounts(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0)
):
    """
    Lista todas as contas com paginação
    
    - **limit**: Número máximo de resultados (1-1000, padrão: 100)
    - **offset**: Offset para paginação (padrão: 0)
    """
    try:
        accounts = await account_service.get_all_accounts(limit=limit, offset=offset)
        return accounts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar contas: {str(e)}"
        )


@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(account_id: str, account_data: AccountUpdate):
    """
    Atualiza dados de uma conta
    
    - **name**: Novo nome (opcional)
    - **email**: Novo email (opcional)
    """
    try:
        account = await account_service.update_account(account_id, account_data)
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conta não encontrada"
            )
        
        return account
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar conta: {str(e)}"
        )


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(account_id: str):
    """
    Deleta uma conta
    """
    try:
        success = await account_service.delete_account(account_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conta não encontrada"
            )
        
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar conta: {str(e)}"
        )