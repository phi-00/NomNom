from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date
from enum import Enum


class TipoAlimentacao(str, Enum):
    """Tipos de alimentação disponíveis"""
    SEM_RESTRICAO = "sem restrições"
    VEGETARIANO = "vegetariano"
    VEGANO = "vegano"
    CELIACO = "celiaco"
    PESCETARIANO = "pescetariano"
    SEM_LACTOSE = "sem lactose"


class Sexo(str, Enum):
    """Sexos disponíveis"""
    MASCULINO = "masculino"
    FEMININO = "feminino"
    OUTRO = "outro"


class UtilizadorCreate(BaseModel):
    """Schema para criação de perfil de utilizador"""
    email: str
    nome: str
    altura: float = Field(..., gt=0, le=300, description="Altura em centímetros")
    data_nascimento: date = Field(..., description="Data de nascimento")
    peso: float = Field(..., gt=0, le=500, description="Peso em quilogramas")
    alimentacao: TipoAlimentacao
    sexo: Sexo
    
    @field_validator('altura')
    @classmethod
    def validate_altura(cls, v):
        if v < 50 or v > 300:
            raise ValueError('Altura deve estar entre 50 e 300 cm')
        return v
    
    @field_validator('peso')
    @classmethod
    def validate_peso(cls, v):
        if v < 20 or v > 500:
            raise ValueError('Peso deve estar entre 20 e 500 kg')
        return v


class UtilizadorUpdate(BaseModel):
    """Schema para atualização de perfil de utilizador"""
    nome: Optional[str] = None
    altura: Optional[float] = Field(None, gt=0, le=300)
    data_nascimento: Optional[date] = None
    peso: Optional[float] = Field(None, gt=0, le=500)
    alimentacao: Optional[TipoAlimentacao] = None
    sexo: Optional[Sexo] = None


class UtilizadorResponse(BaseModel):
    """Schema de resposta com dados do utilizador"""
    email: str
    nome: str
    altura: float
    data_nascimento: date
    peso: float
    alimentacao: str
    sexo: str
    
    class Config:
        from_attributes = True
