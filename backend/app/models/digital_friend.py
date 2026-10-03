from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DigitalFriendSettings(Base):
    __tablename__ = "digital_friend_settings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    language: Mapped[str] = mapped_column(
        String(20),
        default="english",
        nullable=False,
    )

    retry_calls: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    max_retries: Mapped[int] = mapped_column(
        Integer,
        default=3,
        nullable=False,
    )

    retry_interval_minutes: Mapped[int] = mapped_column(
        Integer,
        default=5,
        nullable=False,
    )

    quiet_hours_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    quiet_hours_start: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    quiet_hours_end: Mapped[str | None] = mapped_column(
        String(10),
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