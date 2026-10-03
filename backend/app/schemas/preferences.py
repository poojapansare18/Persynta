from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommunicationPreferencesUpdate(BaseModel):
    whatsapp: bool = False
    email: bool = True
    phone: bool = True
    push: bool = True
    task_reminders: bool = True
    meeting_reminders: bool = True
    follow_ups: bool = True


class CommunicationPreferencesResponse(BaseModel):
    id: int
    user_id: int
    whatsapp: bool
    email: bool
    phone: bool
    push: bool
    task_reminders: bool
    meeting_reminders: bool
    follow_ups: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MorningBriefingUpdate(BaseModel):
    enabled: bool = False
    time: str = "08:00"
    whatsapp: bool = True
    email: bool = True
    phone: bool = False
    include_meetings: bool = True
    include_tasks: bool = True
    include_follow_ups: bool = True
    include_notes: bool = True


class MorningBriefingResponse(BaseModel):
    id: int
    user_id: int
    enabled: bool
    time: str
    whatsapp: bool
    email: bool
    phone: bool
    include_meetings: bool
    include_tasks: bool
    include_follow_ups: bool
    include_notes: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)