from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from src.database import get_supabase_client
from src.schemas.account import AccountResponse, AccountCreate
from src.services.account_service import account_service
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


class RegisterResponse(BaseModel):
    """Schema para resposta de registro"""
    user: AccountResponse
    session: dict
    message: str = "Conta criada com sucesso"


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(account_data: AccountCreate):
    """
    Registra um novo usuário e faz login automático
    
    - **name**: Nome do usuário (2-100 caracteres)
    - **email**: Email válido
    - **password**: Senha (mínimo 6 caracteres)
    
    Retorna os dados do usuário e tokens de autenticação.
    """
    try:
        # Criar conta usando o serviço
        account = await account_service.create_account(account_data)
        
        # Fazer login automático após registro
        auth_response = supabase.auth.sign_in_with_password({
            "email": account_data.email,
            "password": account_data.password
        })
        
        session_data = {
            "access_token": auth_response.session.access_token,
            "refresh_token": auth_response.session.refresh_token,
            "expires_in": auth_response.session.expires_in,
            "token_type": "bearer"
        }
        
        return RegisterResponse(
            user=account,
            session=session_data,
            message="Conta criada com sucesso"
        )
        
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