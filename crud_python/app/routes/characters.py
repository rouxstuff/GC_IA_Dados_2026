from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List, Optional

from app.database.config import get_session
from app.models.got import Character, CharacterCreate, CharacterRead, utcnow

router = APIRouter(prefix="/api/characters", tags=["Characters"])


def get_or_404(session: Session, character_id: str) -> Character:
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character with ID {character_id} not found",
        )
    return character


@router.post("/", response_model=CharacterRead, status_code=status.HTTP_201_CREATED)
def create_character(*, session: Session = Depends(get_session), character: CharacterCreate):
    db_got = Character.model_validate(character)
    session.add(db_got)
    session.commit()
    session.refresh(db_got)
    return db_got


@router.get("/", response_model=List[CharacterRead])
def read_characters(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100,
    vivo: Optional[bool] = None,
):
    query = select(Character)
    if vivo is not None:
        query = query.where(Character.vivo == vivo)
    return session.exec(query.offset(offset).limit(limit)).all()


@router.get("/{character_id}", response_model=CharacterRead)
def read_character(*, session: Session = Depends(get_session), character_id: str):
    return get_or_404(session, character_id)


@router.put("/{character_id}", response_model=CharacterRead)
def update_character(
    *, session: Session = Depends(get_session), character_id: str, character: CharacterCreate
):
    db_character = get_or_404(session, character_id)

    for key, value in character.model_dump().items():
        setattr(db_character, key, value)
    db_character.updated_at = utcnow()

    session.add(db_character)
    session.commit()
    session.refresh(db_character)
    return db_character


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(*, session: Session = Depends(get_session), character_id: str):
    character = get_or_404(session, character_id)
    session.delete(character)
    session.commit()