from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate


router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.get("", response_model=list[NoteResponse])
def list_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = (
        select(Note)
        .where(Note.user_id == current_user.id)
        .order_by(Note.updated_at.desc())
    )

    return list(db.scalars(statement).all())


@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = Note(
        user_id=current_user.id,
        title=data.title,
        content=data.content,
        source=data.source,
        important=data.important,
        memory=data.memory,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return note


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = db.scalar(
        select(Note).where(
            Note.id == note_id,
            Note.user_id == current_user.id,
        )
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return note


@router.patch("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    data: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = db.scalar(
        select(Note).where(
            Note.id == note_id,
            Note.user_id == current_user.id,
        )
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(note, field, value)

    note.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(note)

    return note


@router.post("/{note_id}/remember", response_model=NoteResponse)
def remember_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = db.scalar(
        select(Note).where(
            Note.id == note_id,
            Note.user_id == current_user.id,
        )
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    note.memory = True
    note.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(note)

    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = db.scalar(
        select(Note).where(
            Note.id == note_id,
            Note.user_id == current_user.id,
        )
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    db.delete(note)
    db.commit()

    return None