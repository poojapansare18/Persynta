from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import settings
from app.api.deps import get_current_user
from app.db.session import get_db

from app.models.guest import Guest
from app.models.meeting import Meeting
from app.models.user import User

from app.schemas.meeting import (
    MeetingCreate,
    MeetingResponse,
    MeetingUpdate,
    PublicMeetingChangeRequest,
)

from app.services.email import EmailService
from app.services.email_templates import meeting_confirmation_email

from app.services.google_calendar import (
    GoogleCalendarError,
    GoogleCalendarService,
)

from app.services.security import (
    create_meeting_confirmation_token,
    decode_meeting_confirmation_token,
    create_meeting_cancel_token,
    decode_meeting_cancel_token,
    create_meeting_change_token,
    decode_meeting_change_token,
)


router = APIRouter(
    prefix="/meetings",
    tags=["Meetings"],
)


# ------------------------------------------------------------------
# Shared helper
# ------------------------------------------------------------------

def get_meeting(
    meeting_id: int,
    db: Session,
    user_id: int,
):
    statement = (
        select(Meeting)
        .options(selectinload(Meeting.guests))
        .where(
            Meeting.id == meeting_id,
            Meeting.user_id == user_id,
        )
    )

    return db.scalar(statement)


# ------------------------------------------------------------------
# List meetings
# ------------------------------------------------------------------

@router.get("", response_model=list[MeetingResponse])
def list_meetings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = (
        select(Meeting)
        .options(selectinload(Meeting.guests))
        .where(Meeting.user_id == current_user.id)
        .order_by(Meeting.start_at.asc())
    )

    return list(
        db.scalars(statement).unique().all()
    )


# ------------------------------------------------------------------
# Create meeting
# ------------------------------------------------------------------

@router.post(
    "",
    response_model=MeetingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_meeting(
    data: MeetingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    guests = []

    if data.guest_ids:
        guests = list(
            db.scalars(
                select(Guest).where(
                    Guest.id.in_(data.guest_ids),
                    Guest.user_id == current_user.id,
                )
            ).all()
        )

        if len(guests) != len(set(data.guest_ids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more guests not found",
            )

    if data.start_at >= data.end_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time.",
        )

    meeting = Meeting(
        user_id=current_user.id,
        title=data.title,
        agenda=data.agenda,
        start_at=data.start_at,
        end_at=data.end_at,
        location=data.location,
        meeting_url=data.meeting_url,
        notes=data.notes,
        status=data.status,
        guests=guests,
    )

    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    # --------------------------------------------------------------
    # Create secure action tokens
    # --------------------------------------------------------------

    confirmation_token = create_meeting_confirmation_token(
        meeting_id=meeting.id,
        user_id=current_user.id,
        expires_minutes=30,
    )

    change_token = create_meeting_change_token(
        meeting_id=meeting.id,
        user_id=current_user.id,
        expires_minutes=30,
    )

    cancel_token = create_meeting_cancel_token(
        meeting_id=meeting.id,
        user_id=current_user.id,
        expires_minutes=30,
    )

    # --------------------------------------------------------------
    # Build URLs
    # --------------------------------------------------------------

    confirmation_url = (
        f"{settings.frontend_url}"
        f"/meetings/confirm/{confirmation_token}"
    )

    change_url = (
        f"{settings.frontend_url}"
        f"/meetings/change/{change_token}"
    )

    cancel_url = (
        f"{settings.frontend_url}"
        f"/meetings/cancel/{cancel_token}"
    )

    # --------------------------------------------------------------
    # Build email
    # --------------------------------------------------------------

    html, text = meeting_confirmation_email(
        title=meeting.title,
        agenda=meeting.agenda,
        start_at=meeting.start_at,
        end_at=meeting.end_at,
        meeting_url=meeting.meeting_url,
        confirmation_url=confirmation_url,
        change_url=change_url,
        cancel_url=cancel_url,
    )

    # --------------------------------------------------------------
    # Send email
    # --------------------------------------------------------------

    EmailService().send_email(
        to=current_user.email,
        subject=f"Confirm meeting: {meeting.title}",
        html=html,
        text=text,
    )

    return get_meeting(
        meeting.id,
        db,
        current_user.id,
    )


# ------------------------------------------------------------------
# Get single meeting
# ------------------------------------------------------------------

@router.get(
    "/{meeting_id}",
    response_model=MeetingResponse,
)
def get_single_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = get_meeting(
        meeting_id,
        db,
        current_user.id,
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    return meeting


# ------------------------------------------------------------------
# Authenticated update
# ------------------------------------------------------------------

@router.patch(
    "/{meeting_id}",
    response_model=MeetingResponse,
)
def update_meeting(
    meeting_id: int,
    data: MeetingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = get_meeting(
        meeting_id,
        db,
        current_user.id,
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    if meeting.status == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cancelled meetings cannot be updated",
        )

    updates = data.model_dump(
        exclude_unset=True,
        exclude={"guest_ids"},
    )

    guests = None

    if data.guest_ids is not None:
        guests = list(
            db.scalars(
                select(Guest).where(
                    Guest.id.in_(data.guest_ids),
                    Guest.user_id == current_user.id,
                )
            ).all()
        )

        if len(guests) != len(set(data.guest_ids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more guests not found",
            )

    # Validate time if both are being changed.
    proposed_start = updates.get(
        "start_at",
        meeting.start_at,
    )

    proposed_end = updates.get(
        "end_at",
        meeting.end_at,
    )

    if proposed_start >= proposed_end:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time.",
        )

    # --------------------------------------------------------------
    # Synchronize scheduled meeting with Google Calendar
    # --------------------------------------------------------------

    if (
        meeting.status == "scheduled"
        and meeting.google_calendar_event_id
    ):
        calendar_service = GoogleCalendarService(
            db=db,
            user_id=current_user.id,
        )

        time_changed = (
            proposed_start != meeting.start_at
            or proposed_end != meeting.end_at
        )

        if time_changed:
            try:
                availability = (
                    calendar_service.check_availability_excluding_event(
                        start_at=proposed_start,
                        end_at=proposed_end,
                        exclude_event_id=meeting.google_calendar_event_id,
                    )
                )
            except GoogleCalendarError as exc:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(exc),
                )

            if not availability.get("available", False):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "message": "The selected time is not available.",
                        "busy": availability.get("busy", []),
                    },
                )

        calendar_update = {}

        if "title" in updates:
            calendar_update["title"] = updates["title"]

        if "start_at" in updates:
            calendar_update["start_at"] = updates["start_at"]

        if "end_at" in updates:
            calendar_update["end_at"] = updates["end_at"]

        if "agenda" in updates:
            calendar_update["description"] = updates["agenda"]

        if "location" in updates:
            calendar_update["location"] = updates["location"]

        if guests is not None:
            calendar_update["attendees"] = [
                guest.email
                for guest in guests
                if guest.email
            ]

        if calendar_update:
            try:
                calendar_service.update_event(
                    event_id=meeting.google_calendar_event_id,
                    **calendar_update,
                )
            except GoogleCalendarError as exc:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(exc),
                )

    # --------------------------------------------------------------
    # Apply local changes
    # --------------------------------------------------------------

    for field, value in updates.items():
        setattr(meeting, field, value)

    if guests is not None:
        meeting.guests = guests

    meeting.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(meeting)

    return get_meeting(
        meeting.id,
        db,
        current_user.id,
    )


# ------------------------------------------------------------------
# Authenticated confirm
# ------------------------------------------------------------------

@router.post(
    "/{meeting_id}/confirm",
    response_model=MeetingResponse,
)
def confirm_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = get_meeting(
        meeting_id,
        db,
        current_user.id,
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    if meeting.status == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cancelled meeting cannot be confirmed",
        )

    if meeting.google_calendar_event_id:
        meeting.status = "scheduled"
        meeting.updated_at = datetime.now(timezone.utc)

        db.commit()

        return get_meeting(
            meeting.id,
            db,
            current_user.id,
        )

    calendar_service = GoogleCalendarService(
        db=db,
        user_id=current_user.id,
    )

    try:
        availability = calendar_service.check_availability(
            start_at=meeting.start_at,
            end_at=meeting.end_at,
        )
    except GoogleCalendarError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    if not availability.get("available", False):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "The selected time is no longer available.",
                "busy": availability.get("busy", []),
            },
        )

    attendees = [
        guest.email
        for guest in meeting.guests
        if guest.email
    ]

    try:
        google_event = calendar_service.create_event(
            title=meeting.title,
            start_at=meeting.start_at,
            end_at=meeting.end_at,
            description=meeting.agenda or meeting.notes,
            location=meeting.location,
            attendees=attendees,
            create_meet=True,
            send_updates="all",
        )
    except GoogleCalendarError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    google_event_id = google_event.get("id")

    if not google_event_id:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Google Calendar did not return an event ID.",
        )

    meeting_url = None

    conference_data = (
        google_event.get("conferenceData") or {}
    )

    entry_points = (
        conference_data.get("entryPoints") or []
    )

    for entry_point in entry_points:
        if entry_point.get("entryPointType") == "video":
            meeting_url = entry_point.get("uri")
            break

    meeting.google_calendar_event_id = google_event_id

    if meeting_url:
        meeting.meeting_url = meeting_url

    meeting.status = "scheduled"
    meeting.updated_at = datetime.now(timezone.utc)

    db.commit()

    return get_meeting(
        meeting.id,
        db,
        current_user.id,
    )


# ------------------------------------------------------------------
# Authenticated cancel
# ------------------------------------------------------------------

@router.post(
    "/{meeting_id}/cancel",
    response_model=MeetingResponse,
)
def cancel_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = get_meeting(
        meeting_id,
        db,
        current_user.id,
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    if meeting.google_calendar_event_id:
        calendar_service = GoogleCalendarService(
            db=db,
            user_id=current_user.id,
        )

        try:
            calendar_service.delete_event(
                event_id=meeting.google_calendar_event_id,
                send_updates="all",
            )
        except GoogleCalendarError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            )

    meeting.google_calendar_event_id = None
    meeting.meeting_url = None
    meeting.status = "cancelled"
    meeting.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(meeting)

    return meeting


# ==================================================================
# PUBLIC EMAIL CONFIRMATION
# ==================================================================

@router.get(
    "/confirm/{token}",
    response_model=MeetingResponse,
)
def preview_meeting_from_email(
    token: str,
    db: Session = Depends(get_db),
):
    try:
        user_id, meeting_id = (
            decode_meeting_confirmation_token(token)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired meeting confirmation link.",
        )

    meeting = get_meeting(
        meeting_id,
        db,
        user_id,
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found.",
        )

    if meeting.status == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This meeting has already been cancelled.",
        )

    return meeting


@router.post(
    "/confirm/{token}",
    response_model=MeetingResponse,
)
def confirm_meeting_from_email(
    token: str,
    db: Session = Depends(get_db),
):
    try:
        user_id, meeting_id = (
            decode_meeting_confirmation_token(token)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired meeting confirmation link.",
        )

    meeting = get_meeting(
        meeting_id,
        db,
        user_id,
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found.",
        )

    if meeting.status == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This meeting has already been cancelled.",
        )

    # Prevent duplicate events.
    if meeting.google_calendar_event_id:
        meeting.status = "scheduled"

        db.commit()
        db.refresh(meeting)

        return get_meeting(
            meeting.id,
            db,
            user_id,
        )

    calendar_service = GoogleCalendarService(
        db=db,
        user_id=user_id,
    )

    try:
        availability = calendar_service.check_availability(
            start_at=meeting.start_at,
            end_at=meeting.end_at,
        )
    except GoogleCalendarError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    if not availability.get("available", False):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "The selected time is no longer available.",
                "busy": availability.get("busy", []),
            },
        )

    attendees = [
        guest.email
        for guest in meeting.guests
        if guest.email
    ]

    try:
        google_event = calendar_service.create_event(
            title=meeting.title,
            start_at=meeting.start_at,
            end_at=meeting.end_at,
            description=meeting.agenda or meeting.notes,
            location=meeting.location,
            attendees=attendees,
            create_meet=True,
            send_updates="all",
        )
    except GoogleCalendarError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    google_event_id = google_event.get("id")

    if not google_event_id:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Google Calendar did not return an event ID.",
        )

    meeting.google_calendar_event_id = google_event_id

    meeting.meeting_url = (
        google_event.get("hangoutLink")
        or meeting.meeting_url
    )

    meeting.status = "scheduled"
    meeting.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(meeting)

    return get_meeting(
        meeting.id,
        db,
        user_id,
    )


# ==================================================================
# PUBLIC EMAIL CANCEL
# ==================================================================

@router.get(
    "/cancel/{token}",
    response_model=MeetingResponse,
)
def cancel_meeting_from_email_preview(
    token: str,
    db: Session = Depends(get_db),
):
    try:
        user_id, meeting_id = (
            decode_meeting_cancel_token(token)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired meeting cancellation link.",
        )

    meeting = get_meeting(
        meeting_id,
        db,
        user_id,
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found.",
        )

    if meeting.status == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This meeting has already been cancelled.",
        )

    if meeting.status != "pending_confirmation":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "This meeting can no longer be "
                "cancelled from this link."
            ),
        )

    return meeting


@router.post(
    "/cancel/{token}",
    response_model=MeetingResponse,
)
def cancel_meeting_from_email(
    token: str,
    db: Session = Depends(get_db),
):
    try:
        user_id, meeting_id = (
            decode_meeting_cancel_token(token)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired meeting cancellation link.",
        )

    meeting = get_meeting(
        meeting_id,
        db,
        user_id,
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found.",
        )

    if meeting.status == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This meeting has already been cancelled.",
        )

    if meeting.status != "pending_confirmation":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "This meeting can no longer be "
                "cancelled from this link."
            ),
        )

    if meeting.google_calendar_event_id:
        calendar_service = GoogleCalendarService(
            db=db,
            user_id=user_id,
        )

        try:
            calendar_service.delete_event(
                event_id=meeting.google_calendar_event_id,
                send_updates="all",
            )
        except GoogleCalendarError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            )

    meeting.google_calendar_event_id = None
    meeting.meeting_url = None
    meeting.status = "cancelled"
    meeting.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(meeting)

    return meeting


# ==================================================================
# PUBLIC EMAIL CHANGE
# ==================================================================

@router.get(
    "/change/{token}",
    response_model=MeetingResponse,
)
def change_meeting_from_email_preview(
    token: str,
    db: Session = Depends(get_db),
):
    try:
        user_id, meeting_id = (
            decode_meeting_change_token(token)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired meeting change link.",
        )

    meeting = get_meeting(
        meeting_id,
        db,
        user_id,
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found.",
        )

    if meeting.status == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cancelled meetings cannot be changed.",
        )

    return meeting


@router.post(
    "/change/{token}",
    response_model=MeetingResponse,
)
def change_meeting_from_email(
    token: str,
    data: PublicMeetingChangeRequest,
    db: Session = Depends(get_db),
):
    # --------------------------------------------------------------
    # Validate token
    # --------------------------------------------------------------

    try:
        user_id, meeting_id = (
            decode_meeting_change_token(token)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired meeting change link.",
        )

    # --------------------------------------------------------------
    # Load meeting
    # --------------------------------------------------------------

    meeting = get_meeting(
        meeting_id,
        db,
        user_id,
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found.",
        )

    if meeting.status == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cancelled meetings cannot be changed.",
        )

    # --------------------------------------------------------------
    # Validate time
    # --------------------------------------------------------------

    if data.start_at >= data.end_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time.",
        )

    # --------------------------------------------------------------
    # Resolve guests
    # --------------------------------------------------------------

    normalized_emails = [
        guest.email.strip().lower()
        for guest in data.guests
    ]

    if len(normalized_emails) != len(set(normalized_emails)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duplicate guest email addresses are not allowed.",
        )

    guests = []

    for guest_data in data.guests:
        email = guest_data.email.strip().lower()

        existing_guest = db.scalar(
            select(Guest).where(
                Guest.user_id == user_id,
                Guest.email == email,
            )
        )

        if existing_guest:
            guest = existing_guest
        else:
            guest = Guest(
                user_id=user_id,
                name=guest_data.name.strip(),
                email=email,
            )

            db.add(guest)
            db.flush()

        guests.append(guest)

    # --------------------------------------------------------------
    # Detect time change
    # --------------------------------------------------------------

    time_changed = (
        meeting.start_at != data.start_at
        or meeting.end_at != data.end_at
    )

    # --------------------------------------------------------------
    # Availability
    # --------------------------------------------------------------

    calendar_service = GoogleCalendarService(
        db=db,
        user_id=user_id,
    )

    if time_changed:
        try:
            if (
                meeting.status == "scheduled"
                and meeting.google_calendar_event_id
            ):
                availability = (
                    calendar_service
                    .check_availability_excluding_event(
                        start_at=data.start_at,
                        end_at=data.end_at,
                        exclude_event_id=(
                            meeting.google_calendar_event_id
                        ),
                    )
                )
            else:
                availability = (
                    calendar_service.check_availability(
                        start_at=data.start_at,
                        end_at=data.end_at,
                    )
                )
        except GoogleCalendarError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            )

        if not availability.get("available", False):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": (
                        "The selected time is not available."
                    ),
                    "busy": availability.get("busy", []),
                },
            )

    # --------------------------------------------------------------
    # Update existing Google Calendar event
    # --------------------------------------------------------------

    if (
        meeting.status == "scheduled"
        and meeting.google_calendar_event_id
    ):
        attendees = [
            guest.email
            for guest in guests
            if guest.email
        ]

        try:
            calendar_service.update_event(
                event_id=meeting.google_calendar_event_id,
                title=data.title,
                start_at=data.start_at,
                end_at=data.end_at,
                description=data.agenda,
                location=data.location,
                attendees=attendees,
                send_updates="all",
            )
        except GoogleCalendarError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            )

    # --------------------------------------------------------------
    # Update Persynta
    # --------------------------------------------------------------

    meeting.title = data.title
    meeting.agenda = data.agenda
    meeting.start_at = data.start_at
    meeting.end_at = data.end_at
    meeting.location = data.location
    meeting.guests = guests
    meeting.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(meeting)

    return get_meeting(
        meeting.id,
        db,
        user_id,
    )