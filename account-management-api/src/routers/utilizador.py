from fastapi import APIRouter, HTTPException, status
from src.schemas.utilizador import UtilizadorCreate, UtilizadorResponse, UtilizadorUpdate, TipoAlimentacao, Sexo
from src.database import get_supabase_client

router = APIRouter(
    prefix="/utilizador",
    tags=["utilizador"]
)

supabase = get_supabase_client()


@router.get("/options/enums", status_code=status.HTTP_200_OK)
async def get_enum_options():
    """
    Retorna as opções disponíveis para os enums
    
    Retorna:
    - alimentacao: Lista de opções de alimentação
    - sexo: Lista de opções de sexo
    """
    return {
        "alimentacao": [
            {"value": opt.value, "label": opt.name.replace("_", " ").title()}
            for opt in TipoAlimentacao
        ],
        "sexo": [
            {"value": opt.value, "label": opt.name.title()}
            for opt in Sexo
        ]
    }


def map_db_to_response(db_data: dict) -> dict:
    """Mapeia os dados do banco para o schema de resposta"""
    return {
        "email": db_data.get("email"),
        "nome": db_data.get("nome"),
        "altura": db_data.get("altura"),
        "data_nascimento": db_data.get("data_nascimento"),
        "peso": db_data.get("peso"),
        "alimentacao": db_data.get("alimentacao"),
        "sexo": db_data.get("sexo")
    }


@router.get("/check/{email}", status_code=status.HTTP_200_OK)
async def check_utilizador_exists(email: str):
    """
    Verifica se um utilizador existe na tabela Utilizador pelo email
    
    Retorna:
    - exists: boolean indicando se o perfil existe
    - profile: dados do perfil se existir, null caso contrário
    """
    try:
        response = supabase.table("Utilizador").select("*").eq("email", email).execute()
        
        if response.data and len(response.data) > 0:
            return {
                "exists": True,
                "profile": response.data[0]
            }
        else:
            return {
                "exists": False,
                "profile": None
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao verificar utilizador: {str(e)}"
        )


@router.post("/", response_model=UtilizadorResponse, status_code=status.HTTP_201_CREATED)
async def create_utilizador(utilizador_data: UtilizadorCreate):
    """
    Cria um novo perfil de utilizador na tabela Utilizador
    
    - **email**: Email do usuário (deve corresponder ao email do auth)
    - **nome**: Nome completo
    - **altura**: Altura em centímetros (50-300)
    - **data_nascimento**: Data de nascimento (YYYY-MM-DD)
    - **peso**: Peso em quilogramas (20-500)
    - **alimentacao**: sem_restricao, vegetariano, vegano ou celiaco
    - **sexo**: masculino, feminino ou outro
    """
    try:
        # Verificar se já existe
        existing = supabase.table("Utilizador").select("*").eq("email", utilizador_data.email).execute()
        
        if existing.data and len(existing.data) > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Perfil de utilizador já existe para este email"
            )
        
        # Criar novo utilizador
        utilizador_dict = {
            "email": utilizador_data.email,
            "nome": utilizador_data.nome,
            "altura": utilizador_data.altura,
            "data_nascimento": utilizador_data.data_nascimento.isoformat() if utilizador_data.data_nascimento else None,
            "peso": utilizador_data.peso,
            "alimentacao": utilizador_data.alimentacao.value,
            "sexo": utilizador_data.sexo.value
        }
        
        response = supabase.table("Utilizador").insert(utilizador_dict).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar perfil de utilizador"
            )
        
        return UtilizadorResponse(**map_db_to_response(response.data[0]))
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar utilizador: {str(e)}"
        )


@router.get("/{email}", response_model=UtilizadorResponse)
async def get_utilizador(email: str):
    """
    Busca um utilizador por email
    """
    try:
        response = supabase.table("Utilizador").select("*").eq("email", email).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil de utilizador não encontrado"
            )
        
        return UtilizadorResponse(**map_db_to_response(response.data[0]))
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar utilizador: {str(e)}"
        )


@router.put("/{email}", response_model=UtilizadorResponse)
async def update_utilizador(email: str, utilizador_data: UtilizadorUpdate):
    """
    Atualiza dados de um utilizador existente
    """
    try:
        # Verificar se existe
        existing = supabase.table("Utilizador").select("*").eq("email", email).execute()
        
        if not existing.data or len(existing.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil de utilizador não encontrado"
            )
        
        # Preparar dados para atualização (apenas campos não nulos)
        update_dict = {}
        if utilizador_data.nome is not None:
            update_dict["nome"] = utilizador_data.nome
        if utilizador_data.altura is not None:
            update_dict["altura"] = utilizador_data.altura
        if utilizador_data.data_nascimento is not None:
            update_dict["data_nascimento"] = utilizador_data.data_nascimento.isoformat()
        if utilizador_data.peso is not None:
            update_dict["peso"] = utilizador_data.peso
        if utilizador_data.alimentacao is not None:
            update_dict["alimentacao"] = utilizador_data.alimentacao.value
        if utilizador_data.sexo is not None:
            update_dict["sexo"] = utilizador_data.sexo.value
        
        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum dado fornecido para atualização"
            )
        
        response = supabase.table("Utilizador").update(update_dict).eq("email", email).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar perfil"
            )
        
        return UtilizadorResponse(**map_db_to_response(response.data[0]))
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar utilizador: {str(e)}"
        )
