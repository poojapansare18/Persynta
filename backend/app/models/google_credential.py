from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class GoogleCredential(Base):
    __tablename__ = "google_credentials"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    encrypted_access_token: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    encrypted_refresh_token: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    token_uri: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    scopes: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    token_expiry: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )