from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.guest import Guest
from app.models.user import User
from app.schemas.meeting import GuestCreate, GuestResponse


router = APIRouter(
    prefix="/guests",
    tags=["Guests"],
)


@router.get("", response_model=list[GuestResponse])
def list_guests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = (
        select(Guest)
        .where(Guest.user_id == current_user.id)
        .order_by(Guest.name.asc())
    )

    return list(db.scalars(statement).all())


@router.post(
    "",
    response_model=GuestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_guest(
    data: GuestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = db.scalar(
        select(Guest).where(
            Guest.user_id == current_user.id,
            Guest.email == data.email,
        )
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Guest with this email already exists",
        )

    guest = Guest(
        user_id=current_user.id,
        name=data.name,
        email=data.email,
    )

    db.add(guest)
    db.commit()
    db.refresh(guest)

    return guest