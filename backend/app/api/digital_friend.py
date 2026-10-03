from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.digital_friend import DigitalFriendSettings
from app.models.user import User
from app.schemas.digital_friend import (
    DigitalFriendSettingsResponse,
    DigitalFriendSettingsUpdate,
)


router = APIRouter(
    prefix="/digital-friend",
    tags=["Digital Friend"],
)


@router.get(
    "/settings",
    response_model=DigitalFriendSettingsResponse,
)
def get_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    settings = db.scalar(
        select(DigitalFriendSettings).where(
            DigitalFriendSettings.user_id == current_user.id
        )
    )

    if not settings:
        settings = DigitalFriendSettings(
            user_id=current_user.id,
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return settings


@router.patch(
    "/settings",
    response_model=DigitalFriendSettingsResponse,
)
def update_settings(
    data: DigitalFriendSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    settings = db.scalar(
        select(DigitalFriendSettings).where(
            DigitalFriendSettings.user_id == current_user.id
        )
    )

    if not settings:
        settings = DigitalFriendSettings(
            user_id=current_user.id,
        )
        db.add(settings)

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(settings, field, value)

    settings.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(settings)

    return settings