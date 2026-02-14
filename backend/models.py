from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


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
