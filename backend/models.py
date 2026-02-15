from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


# ========== MODELOS DE USER/AUTENTICAÇÃO ==========

class UserCreate(BaseModel):
    """Modelo para criação de conta"""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    # Adicione mais campos conforme sua base de dados
    # phone: Optional[str] = None
    # avatar_url: Optional[str] = None
    # etc...


class UserResponse(BaseModel):
    """Modelo de resposta após criação/login (sem senha)"""
    id: str
    email: str
    name: str
    created_at: datetime
    # Adicione mais campos conforme necessário
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Modelo para login"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Modelo de resposta do login"""
    user: UserResponse
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"
    message: str
    profile_complete: bool = False


# ========== MODELOS DE EXEMPLO (ITEMS) ==========

class ItemBase(BaseModel):
    """Modelo base para Item (exemplo)"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """Modelo para criar um Item"""
    pass


class ItemUpdate(BaseModel):
    """Modelo para atualizar um Item"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class Item(ItemBase):
    """Modelo completo de Item (com dados do banco)"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
