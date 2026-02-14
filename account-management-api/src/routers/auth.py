from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from src.database import get_supabase_client
from src.schemas.account import AccountResponse
from gotrue.errors import AuthApiError

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

supabase = get_supabase_client()


class LoginRequest(BaseModel):
    """Schema para requisição de login"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Schema para resposta de login"""
    user: AccountResponse
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"
    message: str = "Login realizado com sucesso"


@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    """
    Realiza login do usuário usando Supabase Auth
    
    - **email**: Email do usuário
    - **password**: Senha do usuário
    
    Retorna os tokens de acesso e refresh para autenticação.
    """
    try:
        # Fazer login no Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        
        if not auth_response.user or not auth_response.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas"
            )
        
        # Preparar resposta com dados do usuário
        user_response = AccountResponse(
            id=auth_response.user.id,
            email=auth_response.user.email,
            name=auth_response.user.user_metadata.get("name", ""),
            created_at=auth_response.user.created_at
        )
        
        return LoginResponse(
            user=user_response,
            access_token=auth_response.session.access_token,
            refresh_token=auth_response.session.refresh_token,
            expires_in=auth_response.session.expires_in,
            token_type="bearer",
            message="Login realizado com sucesso"
        )
        
    except AuthApiError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao fazer login: {str(e)}"
        )


@router.post("/logout")
async def logout():
    """
    Realiza logout do usuário
    
    Para fazer logout completo, o frontend deve:
    1. Enviar o token de acesso no header Authorization
    2. Chamar este endpoint
    3. Limpar o token localmente
    """
    try:
        supabase.auth.sign_out()
        return {"message": "Logout realizado com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao fazer logout: {str(e)}"
        )


@router.get("/me", response_model=AccountResponse)
async def get_current_user():
    """
    Retorna dados do usuário atual (requer autenticação)
    
    Para usar este endpoint, envie o access_token no header:
    Authorization: Bearer {access_token}
    
    Nota: Este é um exemplo básico. Para produção, implemente
    middleware de autenticação adequado.
    """
    try:
        user = supabase.auth.get_user()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não autenticado"
            )
        
        return AccountResponse(
            id=user.user.id,
            email=user.user.email,
            name=user.user.user_metadata.get("name", ""),
            created_at=user.user.created_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )