from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DigitalFriendSettingsUpdate(BaseModel):
    phone_number: str | None = None
    language: str = "english"
    retry_calls: bool = True
    max_retries: int = 3
    retry_interval_minutes: int = 5
    quiet_hours_enabled: bool = True
    quiet_hours_start: str | None = None
    quiet_hours_end: str | None = None


class DigitalFriendSettingsResponse(BaseModel):
    id: int
    user_id: int
    phone_number: str | None
    language: str
    retry_calls: bool
    max_retries: int
    retry_interval_minutes: int
    quiet_hours_enabled: bool
    quiet_hours_start: str | None
    quiet_hours_end: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)