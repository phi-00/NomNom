from datetime import datetime
from typing import Optional


class Account:
    """Modelo de Account para o Supabase
    
    O Supabase usa UUID para IDs e não precisa de ORM tradicional.
    Este modelo é usado apenas para tipagem e estrutura de dados.
    """
    
    def __init__(
        self, 
        id: str,
        email: str,
        name: str,
        created_at: datetime,
        updated_at: Optional[datetime] = None
    ):
        self.id = id  # UUID do Supabase Auth
        self.email = email
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<Account(id={self.id}, name={self.name}, email={self.email})>"
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at
        }