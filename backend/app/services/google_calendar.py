from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.google_credential import GoogleCredential
from app.services.google_oauth import decrypt_token, encrypt_token


class GoogleCalendarError(Exception):
    """Raised when a Google Calendar operation fails."""


class GoogleCalendarService:
    """
    Service layer for Google Calendar operations.

    Responsibilities:
    - Load encrypted Google credentials from the database
    - Refresh expired access tokens
    - Persist refreshed tokens
    - Build an authenticated Calendar API client
    - Read/create/update/delete events
    - Check calendar availability
    """

    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id

    # ------------------------------------------------------------------
    # Credential handling
    # ------------------------------------------------------------------

    def _get_google_credential(self) -> GoogleCredential:
        credential = self.db.scalar(
            select(GoogleCredential).where(
                GoogleCredential.user_id == self.user_id
            )
        )

        if not credential:
            raise GoogleCalendarError(
                "Google Calendar is not connected for this user."
            )

        return credential

    def _build_credentials(self) -> Credentials:
        stored = self._get_google_credential()

        access_token = decrypt_token(
            stored.encrypted_access_token
        )

        refresh_token = None

        if stored.encrypted_refresh_token:
            refresh_token = decrypt_token(
                stored.encrypted_refresh_token
            )

        scopes = stored.scopes.split()

        credentials = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri=stored.token_uri,
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
            scopes=scopes,
        )

        if stored.token_expiry:
            credentials.expiry = stored.token_expiry

        # --------------------------------------------------------------
        # Refresh expired credentials
        # --------------------------------------------------------------

        if credentials.expired:

            if not credentials.refresh_token:
                raise GoogleCalendarError(
                    "Google access token has expired and no refresh "
                    "token is available. Reconnect Google Calendar."
                )

            try:
                credentials.refresh(Request())
            except Exception as exc:
                raise GoogleCalendarError(
                    "Failed to refresh Google Calendar credentials."
                ) from exc

            # ----------------------------------------------------------
            # Persist refreshed credentials
            # ----------------------------------------------------------

            stored.encrypted_access_token = encrypt_token(
                credentials.token
            )

            if credentials.refresh_token:
                stored.encrypted_refresh_token = encrypt_token(
                    credentials.refresh_token
                )

            stored.token_expiry = credentials.expiry
            stored.updated_at = datetime.utcnow()

            self.db.commit()

        return credentials

    # ------------------------------------------------------------------
    # Google Calendar client
    # ------------------------------------------------------------------

    def _get_service(self) -> Resource:
        credentials = self._build_credentials()

        try:
            return build(
                "calendar",
                "v3",
                credentials=credentials,
                cache_discovery=False,
            )
        except Exception as exc:
            raise GoogleCalendarError(
                "Could not initialize Google Calendar service."
            ) from exc

    # ------------------------------------------------------------------
    # Calendar information
    # ------------------------------------------------------------------

    def get_primary_calendar(self) -> dict:
        service = self._get_service()

        try:
            return (
                service.calendars()
                .get(calendarId="primary")
                .execute()
            )
        except HttpError as exc:
            raise GoogleCalendarError(
                "Could not retrieve the primary Google Calendar."
            ) from exc

    # ------------------------------------------------------------------
    # List events
    # ------------------------------------------------------------------

    def list_events(
        self,
        time_min: datetime | None = None,
        time_max: datetime | None = None,
        max_results: int = 50,
    ) -> list[dict]:

        service = self._get_service()

        params = {
            "calendarId": "primary",
            "maxResults": max_results,
            "singleEvents": True,
            "orderBy": "startTime",
        }

        if time_min:
            params["timeMin"] = self._to_rfc3339(time_min)

        if time_max:
            params["timeMax"] = self._to_rfc3339(time_max)

        try:
            response = (
                service.events()
                .list(**params)
                .execute()
            )

            return response.get("items", [])

        except HttpError as exc:
            raise GoogleCalendarError(
                "Could not retrieve Google Calendar events."
            ) from exc

    # ------------------------------------------------------------------
    # Get one event
    # ------------------------------------------------------------------

    def get_event(self, event_id: str) -> dict:

        service = self._get_service()

        try:
            return (
                service.events()
                .get(
                    calendarId="primary",
                    eventId=event_id,
                )
                .execute()
            )

        except HttpError as exc:
            raise GoogleCalendarError(
                "Could not retrieve the Google Calendar event."
            ) from exc

    # ------------------------------------------------------------------
    # Create event
    # ------------------------------------------------------------------

    def create_event(
        self,
        title: str,
        start_at: datetime,
        end_at: datetime,
        description: str | None = None,
        location: str | None = None,
        attendees: list[str] | None = None,
        create_meet: bool = False,
        send_updates: str = "all",
        event_id: str | None = None,
    ) -> dict:

        service = self._get_service()

        event = {
            "summary": title,
            "start": {
                "dateTime": self._to_rfc3339(start_at),
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": self._to_rfc3339(end_at),
                "timeZone": "Asia/Kolkata",
            },
        }
 
        if description:
            event["description"] = description

        if location:
            event["location"] = location

        if attendees:
            event["attendees"] = [
                {"email": email}
                for email in attendees
            ]

        # --------------------------------------------------------------
        # Optional Google Meet creation
        # --------------------------------------------------------------

        if create_meet:
            event["conferenceData"] = {
                "createRequest": {
                    "requestId": self._generate_request_id(),
                    "conferenceSolutionKey": {
                        "type": "hangoutsMeet"
                    },
                }
            }

        if event_id:
            event["id"] = event_id

        try:
            return (
                service.events()
                .insert(
                    calendarId="primary",
                    body=event,
                    sendUpdates=send_updates,
                    conferenceDataVersion=1 if create_meet else 0,
                )
                .execute()
            )

        except HttpError as exc:
            raise GoogleCalendarError(
                "Could not create Google Calendar event."
            ) from exc

    # ------------------------------------------------------------------
    # Update event
    # ------------------------------------------------------------------

    _UNSET = object()


    def update_event(
        self,
        event_id: str,
        title: str | None = None,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
        description: str | None | object = _UNSET,
        location: str | None | object = _UNSET,
        attendees: list[str] | None = None,
        send_updates: str = "all",
    ) -> dict:

        service = self._get_service()

        body = {}

        if title is not None:
            body["summary"] = title

        if start_at is not None:
            body["start"] = {
                "dateTime": self._to_rfc3339(start_at),
                "timeZone": "Asia/Kolkata",
           }

        if end_at is not None:
            body["end"] = {
                "dateTime": self._to_rfc3339(end_at),
                "timeZone": "Asia/Kolkata",
           }

        if description is not self._UNSET:
            body["description"] = description

        if location is not self._UNSET:
            body["location"] = location

        if attendees is not None:
            body["attendees"] = [
                {"email": email}
                for email in attendees
            ]

        try:
            return (
                service.events()
                .patch(
                    calendarId="primary",
                    eventId=event_id,
                    body=body,
                    sendUpdates=send_updates,
                )
                .execute()
            )

        except HttpError as exc:
            raise GoogleCalendarError(
                "Could not update Google Calendar event."
            ) from exc

    # ------------------------------------------------------------------
    # Delete event
    # ------------------------------------------------------------------

    def delete_event(
        self,
        event_id: str,
        send_updates: str = "all",
    ) -> None:

        service = self._get_service()

        try:
            (
                service.events()
                .delete(
                    calendarId="primary",
                    eventId=event_id,
                    sendUpdates=send_updates,
                )
                .execute()
            )

        except HttpError as exc:
            raise GoogleCalendarError(
                "Could not delete Google Calendar event."
            ) from exc

    # ------------------------------------------------------------------
    # Free / Busy
    # ------------------------------------------------------------------

    def check_availability(
        self,
        start_at: datetime,
        end_at: datetime,
    ) -> dict:

        service = self._get_service()

        body = {
            "timeMin": self._to_rfc3339(start_at),
            "timeMax": self._to_rfc3339(end_at),
            "items": [
                {
                    "id": "primary"
                }
            ],
        }

        try:
            response = (
                service.freebusy()
                .query(body=body)
                .execute()
            )

            calendars = response.get("calendars", {})
            primary = calendars.get("primary", {})

            busy_periods = primary.get("busy", [])

            return {
                "available": len(busy_periods) == 0,
                "busy": busy_periods,
            }

        except HttpError as exc:
            raise GoogleCalendarError(
                "Could not check Google Calendar availability."
            ) from exc

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _to_rfc3339(value: datetime) -> str:
        """
        Convert a datetime to RFC3339.

        Persynta currently uses Asia/Kolkata as the default
        timezone when a datetime has no timezone information.
        """

        if value.tzinfo is None:
            value = value.replace(
                tzinfo=ZoneInfo("Asia/Kolkata")
            )

        return value.isoformat()

    @staticmethod
    def _generate_request_id() -> str:
        import uuid

        return str(uuid.uuid4())

    def check_availability_excluding_event(
        self,
        start_at: datetime,
        end_at: datetime,
        exclude_event_id: str,
    ) -> dict:
        events = self.list_events(
            start_at=start_at,
            end_at=end_at,
        )

        busy = []

        for event in events:
            if event.get("id") == exclude_event_id:
                continue

            if event.get("status") == "cancelled":
                continue

            if event.get("transparency") == "transparent":
                continue

            event_start = event.get("start", {})
            event_end = event.get("end", {})

            if "dateTime" not in event_start or "dateTime" not in event_end:
                continue

            try:
                existing_start = datetime.fromisoformat(
                    event_start["dateTime"].replace("Z", "+00:00")
                )
                existing_end = datetime.fromisoformat(
                    event_end["dateTime"].replace("Z", "+00:00")
                )
            except ValueError:
                continue

            if (
                start_at < existing_end
                and end_at > existing_start
            ):
                busy.append(
                    {
                        "start": event_start["dateTime"],
                        "end": event_end["dateTime"],
                        "event_id": event.get("id"),
                        "summary": event.get("summary"),
                    }
                )

        return {
            "available": len(busy) == 0,
            "busy": busy,
        }

def check_availability_excluding_event(
    self,
    start_at: datetime,
    end_at: datetime,
    exclude_event_id: str,
) -> dict:

    events = self.list_events(
        start_at=start_at,
        end_at=end_at,
    )

    busy = []

    for event in events:

        if event.get("id") == exclude_event_id:
            continue

        if event.get("status") == "cancelled":
            continue

        if event.get("transparency") == "transparent":
            continue

        event_start = event.get("start", {})
        event_end = event.get("end", {})

        if (
            "dateTime" not in event_start
            or "dateTime" not in event_end
        ):
            continue

        try:
            existing_start = datetime.fromisoformat(
                event_start["dateTime"].replace(
                    "Z",
                    "+00:00",
                )
            )

            existing_end = datetime.fromisoformat(
                event_end["dateTime"].replace(
                    "Z",
                    "+00:00",
                )
            )

        except ValueError:
            continue

        if (
            start_at < existing_end
            and end_at > existing_start
        ):
            busy.append(
                {
                    "start": event_start["dateTime"],
                    "end": event_end["dateTime"],
                    "event_id": event.get("id"),
                    "summary": event.get("summary"),
                }
            )

    return {
        "available": len(busy) == 0,
        "busy": busy,
    }