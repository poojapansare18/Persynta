from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MemoryCreate(BaseModel):
    content: str
    source: str = "conversation"
    confidence: float | None = None


class MemoryResponse(BaseModel):
    id: int
    user_id: int
    content: str
    source: str
    confidence: float | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)