from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.meeting import Meeting
from app.models.user import User
from app.schemas.calendar import (
    CalendarEventResponse,
    CalendarSyncResponse,
)
from app.services.google_calendar import (
    GoogleCalendarError,
    GoogleCalendarService,
)


router = APIRouter(
    prefix="/calendar",
    tags=["Calendar"],
)


# ---------------------------------------------------------------------------
# Persynta local calendar events
# ---------------------------------------------------------------------------

@router.get(
    "/events",
    response_model=list[CalendarEventResponse],
)
def list_calendar_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return Persynta meetings stored in the local database.

    This endpoint remains the application's internal calendar view.
    """

    statement = (
        select(Meeting)
        .where(
            Meeting.user_id == current_user.id,
            Meeting.status != "cancelled",
        )
        .order_by(Meeting.start_at.asc())
    )

    meetings = list(
        db.scalars(statement).all()
    )

    return [
        CalendarEventResponse(
            id=meeting.id,
            title=meeting.title,
            agenda=meeting.agenda,
            start_at=meeting.start_at,
            end_at=meeting.end_at,
            location=meeting.location,
            meeting_url=meeting.meeting_url,
            status=meeting.status,
            google_calendar_event_id=(
                meeting.google_calendar_event_id
            ),
        )
        for meeting in meetings
    ]


# ---------------------------------------------------------------------------
# Google Calendar events
# ---------------------------------------------------------------------------

@router.get(
    "/google-events",
)
def list_google_calendar_events(
    start: datetime | None = Query(default=None),
    end: datetime | None = Query(default=None),
    max_results: int = Query(
        default=50,
        ge=1,
        le=250,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Read events directly from the user's primary Google Calendar.

    This is intentionally separate from /calendar/events.

    /calendar/events
        -> Persynta database

    /calendar/google-events
        -> Google Calendar
    """

    now = datetime.now(timezone.utc)

    if start is None:
        start = now

    if end is None:
        end = start + timedelta(days=30)

    if end <= start:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time.",
        )

    calendar_service = GoogleCalendarService(
        db=db,
        user_id=current_user.id,
    )

    try:
        events = calendar_service.list_events(
            time_min=start,
            time_max=end,
            max_results=max_results,
        )

    except GoogleCalendarError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return {
        "calendar": "primary",
        "start": start,
        "end": end,
        "count": len(events),
        "events": events,
    }


# ---------------------------------------------------------------------------
# Google Calendar availability
# ---------------------------------------------------------------------------

@router.get(
    "/availability",
)
def check_calendar_availability(
    start: datetime = Query(...),
    end: datetime = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Check whether the user's primary Google Calendar is free
    during the requested time period.
    """

    if end <= start:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time.",
        )

    calendar_service = GoogleCalendarService(
        db=db,
        user_id=current_user.id,
    )

    try:
        result = calendar_service.check_availability(
            start_at=start,
            end_at=end,
        )

    except GoogleCalendarError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return {
        "start": start,
        "end": end,
        **result,
    }


# ---------------------------------------------------------------------------
# Google Calendar sync verification
# ---------------------------------------------------------------------------

@router.post(
    "/sync",
    response_model=CalendarSyncResponse,
)
def sync_calendar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Verify that Persynta can read the user's Google Calendar.

    For this first integration stage, we do NOT copy arbitrary
    Google events into the Persynta Meeting table.

    That prevents duplicate meetings and avoids incorrectly
    interpreting external calendar events.

    Actual event synchronization will be added after the
    Google Calendar API connection has been verified.
    """

    calendar_service = GoogleCalendarService(
        db=db,
        user_id=current_user.id,
    )

    now = datetime.now(timezone.utc)
    end = now + timedelta(days=30)

    try:
        google_events = calendar_service.list_events(
            time_min=now,
            time_max=end,
            max_results=250,
        )

    except GoogleCalendarError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return CalendarSyncResponse(
        status="connected",
        message=(
            "Google Calendar connection verified successfully. "
            "Google events were read but not imported into "
            "Persynta yet."
        ),
        events_synced=len(google_events),
    )

@router.delete("/google-events/{event_id}")
def delete_google_calendar_event(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    calendar_service = GoogleCalendarService(
        db=db,
        user_id=current_user.id,
    )

    try:
        calendar_service.delete_event(
            event_id=event_id,
            send_updates="all",
        )
    except GoogleCalendarError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return {
        "status": "deleted",
        "event_id": event_id,
    }