from datetime import datetime
from typing import List

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from habit_tracker.db import Base
from habit_tracker.db.mixins import TimeStampMixin


class Users(Base, TimeStampMixin):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(256), nullable=True, unique=True)
    password: Mapped[str] = mapped_column(String(256), nullable=False)

    habits: Mapped[List["Habits"]] = relationship("Habits", back_populates="user")
    pomodoros: Mapped[List["Pomodoros"]] = relationship("Pomodoros", back_populates="user")

    sessions: Mapped[List["UserSession"]] = relationship("UserSession", back_populates="user")

class UserSession(Base, TimeStampMixin):

    __tablename__ = "user_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    session_token: Mapped[str] = mapped_column(String, unique=True, index=True)
    ip_address: Mapped[str] = mapped_column(String, nullable=True)
    user_agent: Mapped[str] = mapped_column(String, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user: Mapped["Users"] = relationship("Users", back_populates="sessions")