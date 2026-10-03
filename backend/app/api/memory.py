from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.memory import Memory
from app.models.user import User
from app.schemas.memory import MemoryCreate, MemoryResponse


router = APIRouter(
    prefix="/memory",
    tags=["Memory"],
)


@router.get("", response_model=list[MemoryResponse])
def list_memories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = (
        select(Memory)
        .where(Memory.user_id == current_user.id)
        .order_by(Memory.updated_at.desc())
    )

    return list(db.scalars(statement).all())


@router.post(
    "",
    response_model=MemoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_memory(
    data: MemoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    memory = Memory(
        user_id=current_user.id,
        content=data.content,
        source=data.source,
        confidence=data.confidence,
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory


@router.get("/search", response_model=list[MemoryResponse])
def search_memories(
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = (
        select(Memory)
        .where(
            Memory.user_id == current_user.id,
            Memory.content.ilike(f"%{q}%"),
        )
        .order_by(Memory.updated_at.desc())
    )

    return list(db.scalars(statement).all())


@router.get("/{memory_id}", response_model=MemoryResponse)
def get_memory(
    memory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    memory = db.scalar(
        select(Memory).where(
            Memory.id == memory_id,
            Memory.user_id == current_user.id,
        )
    )

    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    return memory