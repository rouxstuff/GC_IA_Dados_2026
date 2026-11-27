from datetime import datetime
import uuid
from sqlmodel import SQLModel, Field
from typing import Optional

def generate_uuid():
    return str(uuid.uuid4())

# Base model
class CharacterBase(SQLModel):
    """Base model for a character."""
    nome: str = Field(index=True)
    casa: str = Field(index=True)
    titulo: Optional[str] = Field(default=None)
    idade: int = Field(default=0, ge=0)  # idade must be non-negative
    vivo: bool = Field(default=True)

#GOT Character model
class Character(CharacterBase, table=True):
    """Character model for database table."""
    id: int = Field(default_factory=generate_uuid, primary_key=True, index=True)

class CharacterCreate(CharacterBase):
    """Model for creating a new character."""
    pass

# Read a character at table
class CharacterRead(CharacterBase):
    """Model for reading a character."""
    id: int
    created_at: datetime
    updated_at: datetime


# Update Model
class CharacterUpdate(SQLModel):
    """Model for updating a character."""
    nome: Optional[str] = None
    casa: Optional[str] = None
    titulo: Optional[str] = None
    idade: Optional[int] = Field(default=None, ge=0)  # idade must be non-negative
    vivo: Optional[bool] = None