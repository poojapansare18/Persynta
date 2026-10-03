from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from googleapiclient.discovery import build
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.models.google_credential import GoogleCredential
from app.models.integration import Integration
from app.models.user import User
from app.schemas.integration import (
    IntegrationResponse,
    IntegrationUpdate,
)
from app.services.google_oauth import (
    create_oauth_flow,
    create_oauth_state,
    encrypt_token,
    generate_code_challenge,
    generate_code_verifier,
    verify_oauth_state,
)


router = APIRouter(
    prefix="/integrations",
    tags=["Integrations"],
)


VALID_PROVIDERS = {
    "google_calendar",
    "whatsapp",
    "email",
    "digital_friend",
}


# ---------------------------------------------------------------------------
# List integrations
# ---------------------------------------------------------------------------

@router.get(
    "",
    response_model=list[IntegrationResponse],
)
def list_integrations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = (
        select(Integration)
        .where(Integration.user_id == current_user.id)
        .order_by(Integration.provider.asc())
    )

    return list(db.scalars(statement).all())


# ---------------------------------------------------------------------------
# Update integration
# ---------------------------------------------------------------------------

@router.patch(
    "/{provider}",
    response_model=IntegrationResponse,
)
def update_integration(
    provider: str,
    data: IntegrationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if provider not in VALID_PROVIDERS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported integration provider",
        )

    integration = db.scalar(
        select(Integration).where(
            Integration.user_id == current_user.id,
            Integration.provider == provider,
        )
    )

    if not integration:
        integration = Integration(
            user_id=current_user.id,
            provider=provider,
        )
        db.add(integration)

    integration.status = data.status
    integration.account_email = data.account_email

    if data.status == "connected":
        integration.connected_at = datetime.utcnow()
    else:
        integration.connected_at = None

    integration.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(integration)

    return integration


# ---------------------------------------------------------------------------
# Start Google Calendar OAuth
# ---------------------------------------------------------------------------

@router.get("/google/authorize")
def google_authorize(
    current_user: User = Depends(get_current_user),
):
    """
    Start the Google Calendar OAuth authorization flow.

    Uses OAuth 2.0 Authorization Code flow with PKCE.
    """

    flow = create_oauth_flow()

    # ---------------------------------------------------------------
    # Generate PKCE verifier
    # ---------------------------------------------------------------

    code_verifier = generate_code_verifier()

    # ---------------------------------------------------------------
    # Generate S256 PKCE challenge
    # ---------------------------------------------------------------

    code_challenge = generate_code_challenge(
        code_verifier
    )

    # ---------------------------------------------------------------
    # Create signed state
    #
    # The state contains:
    # - Persynta user ID
    # - PKCE code verifier
    # - expiration
    # ---------------------------------------------------------------

    state = create_oauth_state(
        current_user.id,
        code_verifier,
    )

    # ---------------------------------------------------------------
    # Generate Google authorization URL
    # ---------------------------------------------------------------

    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
        state=state,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )

    return {
        "authorization_url": authorization_url,
    }


# ---------------------------------------------------------------------------
# Google OAuth callback
# ---------------------------------------------------------------------------

@router.get("/google/callback")
def google_callback(
    code: str | None = Query(default=None),
    state: str | None = Query(default=None),
    error: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    """
    Handle Google's OAuth callback.

    Google redirects the browser here after the user
    approves or rejects Persynta's requested permissions.
    """

    # ---------------------------------------------------------------
    # User rejected authorization
    # ---------------------------------------------------------------

    if error:
        return RedirectResponse(
            url=(
                f"{settings.frontend_url}"
                "/settings/integrations"
                f"?google=error&reason={error}"
            ),
            status_code=303,
        )

    # ---------------------------------------------------------------
    # Validate callback parameters
    # ---------------------------------------------------------------

    if not code or not state:
        raise HTTPException(
            status_code=400,
            detail="Missing Google OAuth code or state",
        )

    # ---------------------------------------------------------------
    # Validate signed state
    #
    # Returns:
    #   user_id
    #   code_verifier
    # ---------------------------------------------------------------

    user_id, code_verifier = verify_oauth_state(state)

    # ---------------------------------------------------------------
    # Create OAuth flow
    # ---------------------------------------------------------------

    flow = create_oauth_flow()

    # ---------------------------------------------------------------
    # Restore the SAME PKCE verifier used when authorization
    # was started.
    # ---------------------------------------------------------------

    flow.code_verifier = code_verifier

    # ---------------------------------------------------------------
    # Exchange authorization code for Google tokens
    # ---------------------------------------------------------------

    try:
        flow.fetch_token(
            code=code,
            code_verifier=code_verifier,
        )

    except Exception as exc:
        print(
            "GOOGLE TOKEN EXCHANGE ERROR:",
            repr(exc),
        )

        raise HTTPException(
            status_code=400,
            detail="Failed to exchange Google authorization code",
        )

    credentials = flow.credentials

    # ---------------------------------------------------------------
    # Validate access token
    # ---------------------------------------------------------------

    if not credentials.token:
        raise HTTPException(
            status_code=400,
            detail="Google did not return an access token",
        )

    # ---------------------------------------------------------------
    # Get Google account email
    # ---------------------------------------------------------------

    try:
        oauth2_service = build(
            "oauth2",
            "v2",
            credentials=credentials,
            cache_discovery=False,
        )

        user_info = (
            oauth2_service
            .userinfo()
            .get()
            .execute()
        )

        account_email = user_info.get("email")

    except Exception as exc:
        print(
            "GOOGLE ACCOUNT INFO ERROR:",
            repr(exc),
        )

        raise HTTPException(
            status_code=400,
            detail="Could not retrieve Google account information",
        )

    if not account_email:
        raise HTTPException(
            status_code=400,
            detail="Google account email was not returned",
        )

    # ---------------------------------------------------------------
    # Encrypt OAuth tokens
    # ---------------------------------------------------------------

    encrypted_access_token = encrypt_token(
        credentials.token
    )

    encrypted_refresh_token = None

    if credentials.refresh_token:
        encrypted_refresh_token = encrypt_token(
            credentials.refresh_token
        )

    token_expiry = credentials.expiry

    # ---------------------------------------------------------------
    # Save OAuth scopes
    # ---------------------------------------------------------------

    scopes = " ".join(
        credentials.scopes or []
    )

    # ---------------------------------------------------------------
    # Save / update Google credentials
    # ---------------------------------------------------------------

    google_credential = db.scalar(
        select(GoogleCredential).where(
            GoogleCredential.user_id == user_id
        )
    )

    if google_credential:

        google_credential.encrypted_access_token = (
            encrypted_access_token
        )

        # Google may not return a refresh token on every
        # subsequent authorization attempt.
        #
        # Therefore, never overwrite an existing refresh
        # token with None.
        if encrypted_refresh_token:
            google_credential.encrypted_refresh_token = (
                encrypted_refresh_token
            )

        google_credential.token_uri = (
            credentials.token_uri
        )

        google_credential.scopes = scopes

        google_credential.token_expiry = (
            token_expiry
        )

        google_credential.updated_at = (
            datetime.utcnow()
        )

    else:

        google_credential = GoogleCredential(
            user_id=user_id,
            encrypted_access_token=(
                encrypted_access_token
            ),
            encrypted_refresh_token=(
                encrypted_refresh_token
            ),
            token_uri=credentials.token_uri,
            scopes=scopes,
            token_expiry=token_expiry,
        )

        db.add(google_credential)

    # ---------------------------------------------------------------
    # Update integration status
    # ---------------------------------------------------------------

    integration = db.scalar(
        select(Integration).where(
            Integration.user_id == user_id,
            Integration.provider == "google_calendar",
        )
    )

    if not integration:

        integration = Integration(
            user_id=user_id,
            provider="google_calendar",
        )

        db.add(integration)

    integration.status = "connected"
    integration.account_email = account_email
    integration.connected_at = datetime.utcnow()
    integration.updated_at = datetime.utcnow()

    # ---------------------------------------------------------------
    # Commit credentials + integration status
    # ---------------------------------------------------------------

    try:
        db.commit()

    except Exception as exc:
        db.rollback()

        print(
            "GOOGLE CREDENTIAL SAVE ERROR:",
            repr(exc),
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to save Google integration",
        )

    # ---------------------------------------------------------------
    # Return user to Persynta frontend
    # ---------------------------------------------------------------

    return RedirectResponse(
        url=(
            f"{settings.frontend_url}"
            "/settings/integrations"
            "?google=connected"
        ),
        status_code=303,
    )


# ---------------------------------------------------------------------------
# Existing Google connection endpoint
# ---------------------------------------------------------------------------

@router.post(
    "/google",
    response_model=IntegrationResponse,
)
def connect_google_calendar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Compatibility endpoint.

    The actual Google OAuth flow starts through:

        GET /integrations/google/authorize
    """

    integration = db.scalar(
        select(Integration).where(
            Integration.user_id == current_user.id,
            Integration.provider == "google_calendar",
        )
    )

    if not integration:
        integration = Integration(
            user_id=current_user.id,
            provider="google_calendar",
        )

        db.add(integration)

    integration.status = "pending"
    integration.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(integration)

    return integration


# ---------------------------------------------------------------------------
# Disconnect integration
# ---------------------------------------------------------------------------

@router.delete(
    "/{provider}",
    response_model=IntegrationResponse,
)
def disconnect_integration(
    provider: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if provider not in VALID_PROVIDERS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported integration provider",
        )

    integration = db.scalar(
        select(Integration).where(
            Integration.user_id == current_user.id,
            Integration.provider == provider,
        )
    )

    if not integration:
        raise HTTPException(
            status_code=404,
            detail="Integration not found",
        )

    # ---------------------------------------------------------------
    # If Google Calendar is disconnected, remove the locally
    # encrypted OAuth credentials as well.
    # ---------------------------------------------------------------

    if provider == "google_calendar":

        google_credential = db.scalar(
            select(GoogleCredential).where(
                GoogleCredential.user_id == current_user.id
            )
        )

        if google_credential:
            db.delete(google_credential)

    # ---------------------------------------------------------------
    # Update integration status
    # ---------------------------------------------------------------

    integration.status = "disconnected"
    integration.account_email = None
    integration.connected_at = None
    integration.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(integration)

    return integration