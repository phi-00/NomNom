from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import uuid


class AccountBase(BaseModel):
    """Schema base para Account"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr


class AccountCreate(AccountBase):
    """Schema para criar uma conta"""
    password: str = Field(..., min_length=6)


class AccountUpdate(BaseModel):
    """Schema para atualizar uma conta"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None


class AccountResponse(AccountBase):
    """Schema de resposta de Account"""
    id: str  # UUID do Supabase Auth
    created_at: datetime
    
    class Config:
        from_attributes = True  # Pydantic v2


class AccountInDB(AccountResponse):
    """Schema de Account no banco de dados"""
    pass