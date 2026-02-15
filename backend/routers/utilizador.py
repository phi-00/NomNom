from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from database import get_supabase_client

router = APIRouter()


# Enums válidos para o banco de dados
SEXO_OPTIONS = [
    {"value": "masculino", "label": "Masculino"},
    {"value": "feminino", "label": "Feminino"},
    {"value": "outro", "label": "Outro"}
]

ALIMENTACAO_OPTIONS = [
    {"value": "sem restrições", "label": "Sem Restrições"},
    {"value": "celiaco", "label": "Celíaco"},
    {"value": "vegetariano", "label": "Vegetariano"},
    {"value": "vegano", "label": "Vegano"},
    {"value": "pescetariano", "label": "Pescetariano"},
    {"value": "sem lactose", "label": "Sem Lactose"}
]


@router.get("/options/enums")
async def get_enum_options():
    """
    Retorna as opções válidas para os campos enum (sexo, alimentacao)
    """
    return {
        "sexo": SEXO_OPTIONS,
        "alimentacao": ALIMENTACAO_OPTIONS
    }


@router.get("/{email}")
async def get_utilizador(email: str):
    """
    Busca os dados de um utilizador pelo email
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("Utilizador").select("*").eq("email", email).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilizador não encontrado"
            )
        
        return response.data[0]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar utilizador: {str(e)}"
        )


@router.put("/{email}")
async def update_utilizador(email: str, data: Dict[str, Any]):
    """
    Atualiza os dados de um utilizador (completa o perfil)
    
    Campos aceitos:
    - nome
    - data_nascimento
    - altura
    - peso
    - sexo (must be one of: masculino, feminino, outro)
    - alimentacao (must be one of: sem restrições, celiaco, vegetariano, vegano, pescetariano, sem lactose)
    """
    try:
        supabase = get_supabase_client()
        
        # Validar valores de enum se fornecidos
        if "sexo" in data and data["sexo"]:
            valid_sexos = [opt["value"] for opt in SEXO_OPTIONS]
            if data["sexo"] not in valid_sexos:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Sexo inválido. Valores aceitos: {', '.join(valid_sexos)}"
                )
        
        if "alimentacao" in data and data["alimentacao"]:
            valid_alimentacoes = [opt["value"] for opt in ALIMENTACAO_OPTIONS]
            if data["alimentacao"] not in valid_alimentacoes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Alimentação inválida. Valores aceitos: {', '.join(valid_alimentacoes)}"
                )
        
        # Preparar dados para atualizar
        update_data = {}
        if "nome" in data:
            update_data["nome"] = data["nome"]
        if "data_nascimento" in data:
            update_data["data_nascimento"] = data["data_nascimento"]
        if "altura" in data:
            update_data["altura"] = data["altura"]
        if "peso" in data:
            update_data["peso"] = data["peso"]
        if "sexo" in data:
            update_data["sexo"] = data["sexo"]
        if "alimentacao" in data:
            update_data["alimentacao"] = data["alimentacao"]
        if "tipo_alimentacao" in data:  # Alias para compatibilidade
            update_data["alimentacao"] = data["tipo_alimentacao"]
        
        # Atualizar no banco de dados
        response = supabase.table("Utilizador").update(update_data).eq("email", email).execute()
        
        if not response.data or len(response.data) == 0:
            # Se não encontrar, pode ser que o utilizador não exista, então insere
            insert_data = {"email": email}
            insert_data.update(update_data)
            response = supabase.table("Utilizador").insert(insert_data).execute()
        
        return {
            "status": "success",
            "message": "Perfil atualizado com sucesso",
            "data": response.data[0] if response.data else insert_data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar perfil: {str(e)}"
        )


@router.post("/{email}/profile")
async def complete_profile(email: str, profile_data: Dict[str, Any]):
    """
    Completa o perfil do utilizador (alias para PUT)
    """
    return await update_utilizador(email, profile_data)


@router.post("")
async def complete_profile_from_request(data: Dict[str, Any]):
    """
    Completa o perfil do utilizador a partir do JSON request
    
    Espera um JSON com:
    - email (obrigatório)
    - nome
    - data_nascimento
    - altura
    - peso
    - sexo
    - alimentacao
    """
    if "email" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email é obrigatório"
        )
    
    email = data.pop("email")  # Remove email do data
    return await update_utilizador(email, data)
