from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)

from app.schemas.note import (
    NoteCreate,
    NoteResponse,
    NoteUpdate,
)

from app.schemas.memory import (
    MemoryCreate,
    MemoryResponse,
)

from app.schemas.meeting import (
    GuestCreate,
    GuestResponse,
    MeetingCreate,
    MeetingResponse,
    MeetingUpdate,
)

from app.schemas.digital_friend import (
    DigitalFriendSettingsResponse,
    DigitalFriendSettingsUpdate,
)

from app.schemas.preferences import (
    CommunicationPreferencesResponse,
    CommunicationPreferencesUpdate,
    MorningBriefingResponse,
    MorningBriefingUpdate,
)

from app.schemas.integration import (
    IntegrationResponse,
    IntegrationUpdate,
)

__all__ = [
    "LoginRequest",
    "RegisterRequest",
    "TokenResponse",
    "UserResponse",

    "TaskCreate",
    "TaskResponse",
    "TaskUpdate",

    "NoteCreate",
    "NoteResponse",
    "NoteUpdate",

    "MemoryCreate",
    "MemoryResponse",

    "GuestCreate",
    "GuestResponse",
    "MeetingCreate",
    "MeetingResponse",
    "MeetingUpdate",

    "DigitalFriendSettingsResponse",
    "DigitalFriendSettingsUpdate",

    "CommunicationPreferencesResponse",
    "CommunicationPreferencesUpdate",
    "MorningBriefingResponse",
    "MorningBriefingUpdate",
    "IntegrationResponse",
    "IntegrationUpdate",
]