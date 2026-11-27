from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List

from app.database.config import get_session
from app.models.got import Character, CharacterCreate, CharacterRead

router = APIRouter(prefix="/api/characters", tags={"Characters"})

@router.post("/", response_model=CharacterRead, status_code=status.HTTP_201_CREATED)
def create_character(*, session: Session = Depends(get_session), character: CharacterCreate):
    """
    Create a new character.
    - **id**: Automatically generated.
    - **nome**: Required.
    - **casa**: Required.
    - **titulo**: Optional.
    - **idade**: Optional. idade must be non-negative
    - **vivo**: Optional. default = True.
    """

    # Convrt ChacracterCreate to Character model
    db_got = Character.from_orm(character)

    # Add to database
    session.add(db_got)
    session.commit()
    session.refresh(db_got)

    return db_got

@router.get("/", response_model=List[CharacterRead])
def read_character(*, session: Session = Depends(get_session), offset: int = 0, limit = 100, vivo: bool = None):
    """
    Retrieve a list of tasks with optional filtering.
    - **offse:**: Number of characters to skip (for pagination).
    - **limit**: Maximum number of characters to return (for pagination).
    - **vivo**: Filter by vivo status.
    """

    query = select(Character)
    
    # Apply vivo status filter if provided
    if vivo is not None:
        query = query.where(Character.vivo == vivo)

    # Apply Pagination
    characters = session.exec(query.offset(offset).limit(limit)).all()
    return characters

@router.get("/{character_id}", response_model=CharacterRead)
def read_character (*, session: Session = Depends(get_session), character_id: int):
    """
    Retrieve a specific character by ID.

    - **character_id**: Unique identifier of the character.
    """
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Character with ID {character_id} not found")
    return character

@router.put("/{character_id}", response_model=CharacterRead)
def update_character(*, session: Session = Depends(get_session), character_id: int, character: CharacterCreate):
    """
    Update a charactr completely.

    - **character_id**: The unique identifier of the character.
    - Request body: All character fields (even unchanged ones).
    """
    db_character = session.get(Character, character_id)
    if not db_character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Character with ID {character_id} not found")

    # Update all attribures
    character_data = character.dict()
    for key, value in character_data.items():
        setattr(db_character, key, value)

    # Update in database
    session.add(db_character)
    session.commit()
    session.refresh(db_character)

    return db_character

@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(*, session: Session = Depends(get_session), character_id: int):
    """
    Delete a character.

    - **character_id**: The unique identifier of the character.
    """
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Character with {character_id} not found")

    # Delete from database
    session.delete(character)
    session.commit()

    # Return no content
    return None