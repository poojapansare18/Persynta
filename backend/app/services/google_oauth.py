from datetime import datetime, timedelta, timezone
import base64
import hashlib
import secrets

from cryptography.fernet import Fernet
from fastapi import HTTPException
from google_auth_oauthlib.flow import Flow
from jose import JWTError, jwt

from app.core.config import settings


GOOGLE_SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.freebusy",
]

OAUTH_STATE_EXPIRE_MINUTES = 10


def get_fernet() -> Fernet:
    if not settings.encryption_key:
        raise RuntimeError("ENCRYPTION_KEY is not configured")

    return Fernet(settings.encryption_key.encode())


def encrypt_token(token: str) -> str:
    return get_fernet().encrypt(token.encode()).decode()


def decrypt_token(token: str) -> str:
    return get_fernet().decrypt(token.encode()).decode()


def create_oauth_flow() -> Flow:
    if not settings.google_client_id:
        raise RuntimeError("GOOGLE_CLIENT_ID is not configured")

    if not settings.google_client_secret:
        raise RuntimeError("GOOGLE_CLIENT_SECRET is not configured")

    client_config = {
        "web": {
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [settings.google_redirect_uri],
        }
    }

    flow = Flow.from_client_config(
        client_config,
        scopes=GOOGLE_SCOPES,
    )

    flow.redirect_uri = settings.google_redirect_uri

    return flow


def generate_code_verifier() -> str:
    """
    Generate a PKCE code verifier.
    """
    return secrets.token_urlsafe(64)


def generate_code_challenge(code_verifier: str) -> str:
    """
    Generate an S256 PKCE code challenge.
    """
    digest = hashlib.sha256(
        code_verifier.encode("ascii")
    ).digest()

    return base64.urlsafe_b64encode(
        digest
    ).rstrip(b"=").decode("ascii")


def create_oauth_state(
    user_id: int,
    code_verifier: str,
) -> str:
    """
    Create a signed OAuth state containing the user ID
    and PKCE verifier.

    The state is signed with the application's JWT secret,
    so it cannot be modified without detection.
    """
    now = datetime.now(timezone.utc)

    payload = {
        "user_id": user_id,
        "purpose": "google_calendar_oauth",
        "code_verifier": code_verifier,
        "iat": int(now.timestamp()),
        "exp": int(
            (
                now
                + timedelta(minutes=OAUTH_STATE_EXPIRE_MINUTES)
            ).timestamp()
        ),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def verify_oauth_state(state: str) -> tuple[int, str]:
    """
    Validate the signed OAuth state and return:

    (user_id, code_verifier)
    """
    try:
        payload = jwt.decode(
            state,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )

        if payload.get("purpose") != "google_calendar_oauth":
            raise HTTPException(
                status_code=400,
                detail="Invalid OAuth state",
            )

        user_id = payload.get("user_id")
        code_verifier = payload.get("code_verifier")

        if not user_id or not code_verifier:
            raise HTTPException(
                status_code=400,
                detail="Invalid OAuth state",
            )

        return int(user_id), str(code_verifier)

    except JWTError:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OAuth state",
        )