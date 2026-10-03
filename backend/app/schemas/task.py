from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    due_at: datetime | None = None

    follow_up_enabled: bool = False
    follow_up_at: datetime | None = None

    retry_enabled: bool = False
    max_retries: int | None = None
    retry_interval_minutes: int | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    due_at: datetime | None = None

    follow_up_enabled: bool | None = None
    follow_up_at: datetime | None = None

    retry_enabled: bool | None = None
    max_retries: int | None = None
    retry_interval_minutes: int | None = None


class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    status: str
    due_at: datetime | None

    follow_up_enabled: bool
    follow_up_at: datetime | None

    retry_enabled: bool
    max_retries: int | None
    retry_interval_minutes: int | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)