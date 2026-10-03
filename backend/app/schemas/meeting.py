from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class GuestCreate(BaseModel):
    name: str
    email: EmailStr


class GuestResponse(BaseModel):
    id: int
    user_id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class MeetingCreate(BaseModel):
    title: str
    agenda: str | None = None
    start_at: datetime
    end_at: datetime
    location: str | None = None
    meeting_url: str | None = None
    notes: str | None = None
    status: str = "pending_confirmation"
    guest_ids: list[int] = []


class MeetingUpdate(BaseModel):
    title: str | None = None
    agenda: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    location: str | None = None
    meeting_url: str | None = None
    notes: str | None = None
    status: str | None = None
    guest_ids: list[int] | None = None


class MeetingResponse(BaseModel):
    id: int
    user_id: int
    title: str
    agenda: str | None
    start_at: datetime
    end_at: datetime
    location: str | None
    meeting_url: str | None
    notes: str | None
    status: str
    google_calendar_event_id: str | None
    guests: list[GuestResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PublicGuestChange(BaseModel):
    name: str
    email: EmailStr


class PublicMeetingChangeRequest(BaseModel):
    title: str
    agenda: str | None = None
    start_at: datetime
    end_at: datetime
    location: str | None = None
    guests: list[PublicGuestChange] = []