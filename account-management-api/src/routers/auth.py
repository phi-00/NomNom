from fastapi import APIRouter, HTTPException, status, Header
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
    profile_complete: bool = False


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
        
        # Verificar se existe perfil completo na tabela Utilizador
        profile_complete = False
        try:
            utilizador_response = supabase.table("Utilizador").select("*").eq("email", credentials.email).execute()
            profile_complete = bool(utilizador_response.data and len(utilizador_response.data) > 0)
        except Exception as e:
            print(f"Aviso: Erro ao verificar perfil de utilizador: {str(e)}")
            profile_complete = False
        
        return LoginResponse(
            user=user_response,
            access_token=auth_response.session.access_token,
            refresh_token=auth_response.session.refresh_token,
            expires_in=auth_response.session.expires_in,
            token_type="bearer",
            message="Login realizado com sucesso",
            profile_complete=profile_complete
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


class UpdateNameRequest(BaseModel):
    """Schema para atualizar nome do usuário"""
    email: EmailStr
    name: str


@router.post("/update-name")
async def update_name(data: UpdateNameRequest, authorization: str = Header(None)):
    """
    Atualiza o nome do utilizador
    
    Requer autenticação via Bearer token
    
    - **email**: Email do utilizador
    - **name**: Novo nome (2-100 caracteres)
    """
    try:
        # Validar token
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This endpoint requires a valid Bearer token"
            )
        
        token = authorization[7:]  # Remove "Bearer " prefix
        
        # Validar comprimento do nome
        if len(data.name.strip()) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O nome deve ter pelo menos 2 caracteres"
            )
        
        if len(data.name.strip()) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O nome não pode exceder 100 caracteres"
            )
        
        # Usar Supabase para obter usuário com o token
        from supabase import create_client
        from src.config import get_settings
        
        settings = get_settings()
        supabase_auth = create_client(settings.supabase_url, settings.supabase_key)
        
        try:
            # Obter usuário com o token
            user = supabase_auth.auth.get_user(token)
            
            if not user or not user.user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido ou expirado"
                )
            
            user_id = user.user.id
            
            # Atualizar metadata do usuário usando admin API
            supabase_auth.auth.admin.update_user_by_id(
                user_id,
                {"user_metadata": {"name": data.name.strip()}}
            )
            
            return {
                "message": "Nome atualizado com sucesso",
                "name": data.name.strip(),
                "email": user.user.email
            }
        except Exception as e:
            print(f"Erro ao atualizar nome: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Erro ao verificar token: {str(e)}"
            )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Erro geral: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao atualizar nome: {str(e)}"
        )


class ProfilePictureUpdate(BaseModel):
    """Schema para atualizar foto de perfil"""
    profile_picture: str  # Base64 encoded image
    email: EmailStr


@router.post("/profile-picture")
async def update_profile_picture(data: ProfilePictureUpdate, authorization: str = Header(None)):
    """
    Atualiza a foto de perfil do utilizador
    
    Requer autenticação via Bearer token
    
    Recebe a imagem em base64 e armazena nos metadados do usuário
    """
    try:
        # Validar token
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This endpoint requires a valid Bearer token"
            )
        
        token = authorization[7:]  # Remove "Bearer " prefix
        
        # Validar tamanho aproximado (base64 é ~1.33x maior)
        if len(data.profile_picture) > 6.67 * 1024 * 1024:  # ~5MB em base64
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Imagem muito grande. Máximo 5MB"
            )
        
        # Usar Supabase para obter usuário com o token
        from supabase import create_client
        from src.config import get_settings
        
        settings = get_settings()
        supabase_auth = create_client(settings.supabase_url, settings.supabase_key)
        
        try:
            # Obter usuário com o token
            user = supabase_auth.auth.get_user(token)
            
            if not user or not user.user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido ou expirado"
                )
            
            user_id = user.user.id
            
            # Atualizar metadata com a foto
            supabase_auth.auth.admin.update_user_by_id(
                user_id,
                {"user_metadata": {"profile_picture": data.profile_picture}}
            )
            
            return {
                "message": "Foto de perfil atualizada com sucesso",
                "profile_picture": data.profile_picture
            }
        except Exception as e:
            print(f"Erro ao atualizar foto: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Erro ao verificar token: {str(e)}"
            )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Erro geral: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao atualizar foto de perfil: {str(e)}"
        )