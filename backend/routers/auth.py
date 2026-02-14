from fastapi import APIRouter, HTTPException, status
from models import UserCreate, UserResponse, LoginRequest, LoginResponse
from database import get_supabase_client
from gotrue.errors import AuthApiError

router = APIRouter()
supabase = get_supabase_client()


@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Registra um novo usuário e retorna os dados com token
    """
    try:
        # Criar usuário no Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password,
            "options": {
                "data": {
                    "name": user_data.name,
                }
            }
        })
        
        if not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar conta. Verifique os dados fornecidos."
            )
        
        user_response = UserResponse(
            id=auth_response.user.id,
            email=auth_response.user.email,
            name=user_data.name,
            created_at=auth_response.user.created_at
        )
        
        return LoginResponse(
            user=user_response,
            session={
                "access_token": auth_response.session.access_token if auth_response.session else "",
                "refresh_token": auth_response.session.refresh_token if auth_response.session else "",
                "expires_in": auth_response.session.expires_in if auth_response.session else 0,
                "token_type": auth_response.session.token_type if auth_response.session else "bearer"
            },
            message="Conta criada com sucesso"
        )
        
    except AuthApiError as e:
        if "already registered" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este email já está registrado."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro de autenticação: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar conta: {str(e)}"
        )


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_account(user_data: UserCreate):
    """
    Cria uma nova conta de usuário
    
    O Supabase Auth criará o usuário automaticamente.
    Você pode adicionar dados adicionais em uma tabela 'profiles' ou 'users'.
    
    Personalize este endpoint conforme os campos da sua base de dados.
    """
    try:
        # Criar usuário no Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password,
            "options": {
                "data": {
                    "name": user_data.name,
                    # Adicione mais campos aqui conforme necessário
                    # "phone": user_data.phone,
                    # "avatar_url": user_data.avatar_url,
                }
            }
        })
        
        if not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar conta. Verifique os dados fornecidos."
            )
        
        # Opcional: Inserir dados adicionais em tabela customizada
        # Exemplo: se você tem uma tabela 'profiles' com mais informações
        # profile_data = {
        #     "id": auth_response.user.id,
        #     "name": user_data.name,
        #     "email": user_data.email,
        #     # outros campos...
        # }
        # supabase.table("profiles").insert(profile_data).execute()
        
        # Preparar resposta
        user_response = UserResponse(
            id=auth_response.user.id,
            email=auth_response.user.email,
            name=user_data.name,
            created_at=auth_response.user.created_at
        )
        
        return user_response
        
    except AuthApiError as e:
        # Erros específicos do Supabase Auth
        if "already registered" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este email já está registrado."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro de autenticação: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar conta: {str(e)}"
        )


@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    """
    Realiza login do usuário
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
        
        # Buscar dados adicionais do usuário se necessário
        # Por exemplo, de uma tabela 'profiles'
        # profile = supabase.table("profiles").select("*").eq("id", auth_response.user.id).execute()
        
        user_response = UserResponse(
            id=auth_response.user.id,
            email=auth_response.user.email,
            name=auth_response.user.user_metadata.get("name", ""),
            created_at=auth_response.user.created_at
        )
        
        return LoginResponse(
            user=user_response,
            session={
                "access_token": auth_response.session.access_token,
                "refresh_token": auth_response.session.refresh_token,
                "expires_in": auth_response.session.expires_in,
                "token_type": auth_response.session.token_type
            },
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


@router.get("/me", response_model=UserResponse)
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
        
        return UserResponse(
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
