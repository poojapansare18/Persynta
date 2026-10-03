from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> int:
    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )

    return int(payload["sub"])

def create_meeting_confirmation_token(
    meeting_id: int,
    user_id: int,
    expires_minutes: int = 30,
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes
    )

    payload = {
        "sub": str(user_id),
        "meeting_id": meeting_id,
        "purpose": "meeting_confirmation",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def decode_meeting_confirmation_token(token: str) -> tuple[int, int]:
    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )

    if payload.get("purpose") != "meeting_confirmation":
        raise ValueError("Invalid meeting confirmation token.")

    user_id = int(payload["sub"])
    meeting_id = int(payload["meeting_id"])

    return user_id, meeting_id


def create_meeting_cancel_token(
    meeting_id: int,
    user_id: int,
    expires_minutes: int = 30,
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes
    )

    payload = {
        "sub": str(user_id),
        "meeting_id": meeting_id,
        "purpose": "meeting_cancel",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def decode_meeting_cancel_token(token: str) -> tuple[int, int]:
    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )

    if payload.get("purpose") != "meeting_cancel":
        raise ValueError("Invalid meeting cancellation token.")

    user_id = int(payload["sub"])
    meeting_id = int(payload["meeting_id"])

    return user_id, meeting_id

def create_meeting_change_token(
    meeting_id: int,
    user_id: int,
    expires_minutes: int = 30,
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)

    payload = {
        "sub": str(user_id),
        "meeting_id": meeting_id,
        "purpose": "meeting_change",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def decode_meeting_change_token(token: str) -> tuple[int, int]:
    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )

    if payload.get("purpose") != "meeting_change":
        raise ValueError("Invalid meeting change token.")

    user_id = int(payload["sub"])
    meeting_id = int(payload["meeting_id"])

    return user_id, meeting_id