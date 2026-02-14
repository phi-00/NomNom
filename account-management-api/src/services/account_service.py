from typing import Optional, List
from src.database import get_supabase_client
from src.schemas.account import AccountCreate, AccountResponse, AccountUpdate
from gotrue.errors import AuthApiError


class AccountService:
    """Serviço para gerenciar contas no Supabase"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
    
    async def create_account(self, account_data: AccountCreate) -> AccountResponse:
        """
        Cria uma nova conta usando Supabase Auth
        
        Args:
            account_data: Dados da conta a ser criada
            
        Returns:
            AccountResponse com os dados da conta criada
            
        Raises:
            AuthApiError: Se houver erro na criação da conta
        """
        try:
            # Criar usuário no Supabase Auth
            auth_response = self.supabase.auth.sign_up({
                "email": account_data.email,
                "password": account_data.password,
                "options": {
                    "data": {
                        "name": account_data.name,
                    }
                }
            })
            
            if not auth_response.user:
                raise ValueError("Erro ao criar conta. Verifique os dados fornecidos.")
            
            # Preparar resposta
            return AccountResponse(
                id=auth_response.user.id,
                email=auth_response.user.email,
                name=account_data.name,
                created_at=auth_response.user.created_at
            )
            
        except AuthApiError as e:
            if "already registered" in str(e).lower():
                raise ValueError("Este email já está registrado.")
            raise ValueError(f"Erro de autenticação: {str(e)}")
    
    async def get_account_by_id(self, account_id: str) -> Optional[AccountResponse]:
        """
        Busca uma conta por ID
        
        Args:
            account_id: UUID da conta
            
        Returns:
            AccountResponse ou None se não encontrado
        """
        try:
            # Buscar na tabela profiles (você precisa criar esta tabela no Supabase)
            response = self.supabase.table("profiles").select("*").eq("id", account_id).execute()
            
            if not response.data:
                return None
            
            profile = response.data[0]
            return AccountResponse(
                id=profile["id"],
                email=profile["email"],
                name=profile["name"],
                created_at=profile["created_at"]
            )
        except Exception as e:
            print(f"Erro ao buscar conta: {str(e)}")
            return None
    
    async def get_all_accounts(self, limit: int = 100, offset: int = 0) -> List[AccountResponse]:
        """
        Lista todas as contas
        
        Args:
            limit: Número máximo de registros
            offset: Offset para paginação
            
        Returns:
            Lista de AccountResponse
        """
        try:
            response = self.supabase.table("profiles").select("*").range(offset, offset + limit - 1).execute()
            
            return [
                AccountResponse(
                    id=profile["id"],
                    email=profile["email"],
                    name=profile["name"],
                    created_at=profile["created_at"]
                )
                for profile in response.data
            ]
        except Exception as e:
            print(f"Erro ao listar contas: {str(e)}")
            return []
    
    async def update_account(self, account_id: str, account_data: AccountUpdate) -> Optional[AccountResponse]:
        """
        Atualiza dados de uma conta
        
        Args:
            account_id: UUID da conta
            account_data: Dados para atualizar
            
        Returns:
            AccountResponse atualizado ou None se não encontrado
        """
        try:
            # Preparar dados para atualização
            update_data = account_data.model_dump(exclude_unset=True)
            
            if not update_data:
                # Nenhum campo para atualizar
                return await self.get_account_by_id(account_id)
            
            # Atualizar na tabela profiles
            response = self.supabase.table("profiles").update(update_data).eq("id", account_id).execute()
            
            if not response.data:
                return None
            
            profile = response.data[0]
            return AccountResponse(
                id=profile["id"],
                email=profile["email"],
                name=profile["name"],
                created_at=profile["created_at"]
            )
        except Exception as e:
            print(f"Erro ao atualizar conta: {str(e)}")
            return None
    
    async def delete_account(self, account_id: str) -> bool:
        """
        Deleta uma conta
        
        Args:
            account_id: UUID da conta
            
        Returns:
            True se deletado com sucesso, False caso contrário
        """
        try:
            # Deletar da tabela profiles
            response = self.supabase.table("profiles").delete().eq("id", account_id).execute()
            return True
        except Exception as e:
            print(f"Erro ao deletar conta: {str(e)}")
            return False


# Instância singleton do serviço
account_service = AccountService()