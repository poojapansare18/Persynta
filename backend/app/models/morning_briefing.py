from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class MorningBriefingSettings(Base):
    __tablename__ = "morning_briefing_settings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    time: Mapped[str] = mapped_column(
        String(10),
        default="08:00",
        nullable=False,
    )

    whatsapp: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    email: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    phone: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    include_meetings: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    include_tasks: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    include_follow_ups: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    include_notes: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
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