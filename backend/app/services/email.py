from typing import Iterable

from app.core.config import settings


class EmailService:
    """
    Email delivery service for Persynta.

    The service currently uses a console implementation for development.
    A real provider can be plugged in later without changing the callers.
    """

    def send_email(
        self,
        to: str | Iterable[str],
        subject: str,
        html: str,
        text: str | None = None,
    ) -> None:
        recipients = [to] if isinstance(to, str) else list(to)

        if not recipients:
            raise ValueError("At least one recipient is required.")

        if settings.email_provider == "console":
            self._send_console(
                recipients=recipients,
                subject=subject,
                html=html,
                text=text,
            )
            return

        raise RuntimeError(
            f"Unsupported email provider: {settings.email_provider}"
        )

    def _send_console(
        self,
        recipients: list[str],
        subject: str,
        html: str,
        text: str | None,
    ) -> None:
        print("=" * 60)
        print("PERSYNTA EMAIL")
        print("=" * 60)
        print(f"From: {settings.email_from}")
        print(f"To: {', '.join(recipients)}")
        print(f"Subject: {subject}")
        print("-" * 60)
        print(text or html)
        print("=" * 60)