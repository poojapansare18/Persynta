from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.communication_preferences import CommunicationPreferences
from app.models.morning_briefing import MorningBriefingSettings
from app.models.user import User
from app.schemas.preferences import (
    CommunicationPreferencesResponse,
    CommunicationPreferencesUpdate,
    MorningBriefingResponse,
    MorningBriefingUpdate,
)


router = APIRouter(
    prefix="/preferences",
    tags=["Preferences"],
)


@router.get(
    "/communication",
    response_model=CommunicationPreferencesResponse,
)
def get_communication_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    preferences = db.scalar(
        select(CommunicationPreferences).where(
            CommunicationPreferences.user_id == current_user.id
        )
    )

    if not preferences:
        preferences = CommunicationPreferences(
            user_id=current_user.id,
        )
        db.add(preferences)
        db.commit()
        db.refresh(preferences)

    return preferences


@router.patch(
    "/communication",
    response_model=CommunicationPreferencesResponse,
)
def update_communication_preferences(
    data: CommunicationPreferencesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    preferences = db.scalar(
        select(CommunicationPreferences).where(
            CommunicationPreferences.user_id == current_user.id
        )
    )

    if not preferences:
        preferences = CommunicationPreferences(
            user_id=current_user.id,
        )
        db.add(preferences)

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(preferences, field, value)

    preferences.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(preferences)

    return preferences


@router.get(
    "/morning-briefing",
    response_model=MorningBriefingResponse,
)
def get_morning_briefing(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    briefing = db.scalar(
        select(MorningBriefingSettings).where(
            MorningBriefingSettings.user_id == current_user.id
        )
    )

    if not briefing:
        briefing = MorningBriefingSettings(
            user_id=current_user.id,
        )
        db.add(briefing)
        db.commit()
        db.refresh(briefing)

    return briefing


@router.patch(
    "/morning-briefing",
    response_model=MorningBriefingResponse,
)
def update_morning_briefing(
    data: MorningBriefingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    briefing = db.scalar(
        select(MorningBriefingSettings).where(
            MorningBriefingSettings.user_id == current_user.id
        )
    )

    if not briefing:
        briefing = MorningBriefingSettings(
            user_id=current_user.id,
        )
        db.add(briefing)

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(briefing, field, value)

    briefing.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(briefing)

    return briefing