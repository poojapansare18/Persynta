from datetime import datetime

from pydantic import BaseModel, ConfigDict


class IntegrationUpdate(BaseModel):
    status: str
    account_email: str | None = None


class IntegrationResponse(BaseModel):
    id: int
    user_id: int
    provider: str
    status: str
    account_email: str | None
    connected_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)