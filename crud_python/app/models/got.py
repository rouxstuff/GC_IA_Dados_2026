import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


# Base model
class CharacterBase(SQLModel):
    """Base model for a character."""
    nome: str = Field(index=True)
    casa: str = Field(index=True)
    titulo: Optional[str] = Field(default=None)
    idade: int = Field(default=0, ge=0)  # idade must be non-negative
    vivo: bool = Field(default=True)


# GOT Character model (database table)
class Character(CharacterBase, table=True):
    """Character model for database table."""
    id: str = Field(default_factory=generate_uuid, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=utcnow, nullable=False)


# Create model
class CharacterCreate(CharacterBase):
    """Model for creating a new character."""
    pass


# Read model
class CharacterRead(CharacterBase):
    """Model for reading a character."""
    id: str
    created_at: datetime
    updated_at: datetime


# Update model
class CharacterUpdate(SQLModel):
    """Model for updating a character."""
    nome: Optional[str] = None
    casa: Optional[str] = None
    titulo: Optional[str] = None
    idade: Optional[int] = Field(default=None, ge=0)  # idade must be non-negative
    vivo: Optional[bool] = None