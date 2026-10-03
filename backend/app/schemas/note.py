from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
    title: str
    content: str
    source: str = "written"
    important: bool = False
    memory: bool = False


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    source: str | None = None
    important: bool | None = None
    memory: bool | None = None


class NoteResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    source: str
    important: bool
    memory: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)