from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CommunicationPreferences(Base):
    __tablename__ = "communication_preferences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    whatsapp: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    email: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    phone: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    push: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    task_reminders: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    meeting_reminders: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    follow_ups: Mapped[bool] = mapped_column(
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