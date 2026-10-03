from datetime import datetime

from pydantic import BaseModel


class CalendarEventResponse(BaseModel):
    id: int
    title: str
    agenda: str | None
    start_at: datetime
    end_at: datetime
    location: str | None
    meeting_url: str | None
    status: str
    google_calendar_event_id: str | None


class CalendarSyncResponse(BaseModel):
    status: str
    message: str
    events_synced: int