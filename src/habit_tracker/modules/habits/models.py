import datetime
from typing import List

from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint, Date, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import mapped_column, Mapped, relationship
from habit_tracker.db import Base
from habit_tracker.modules.pomodoros.models import Pomodoros
from habit_tracker.users.models import Users
from habit_tracker.db.mixins import TimeStampMixin


class Habits(Base, TimeStampMixin):
    __tablename__ = "habits"

    __table_args__ = (
        UniqueConstraint("user_id", "title", name="unique_habit_id_title"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    color: Mapped[str] = mapped_column(String(125), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String(25), nullable=False)
    icon_url: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    current_streak: Mapped[int] = mapped_column(Integer, nullable=True)
    best_streak: Mapped[int] = mapped_column(Integer, nullable=True)
    last_completed_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)

    days_to_log: Mapped[list] = mapped_column(ARRAY(Integer), nullable=False)
    logs_to_complete: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("1"))

    user: Mapped["Users"] = relationship("Users", back_populates="habits")
    habit_logs: Mapped[List["HabitLogs"]] = relationship("HabitLogs", back_populates="habit")
    habit_completions: Mapped[List["HabitCompletion"]] = relationship("HabitCompletion", back_populates="habit")
    pomodoros: Mapped[List["Pomodoros"]] = relationship("Pomodoros", back_populates="habit")

class HabitLogs(Base, TimeStampMixin):
    __tablename__ = "habit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"))
    log_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    habit: Mapped["Habits"] = relationship("Habits", back_populates="habit_logs")


class HabitCompletion(Base, TimeStampMixin):
    __tablename__ = "habit_completions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"))
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    habit: Mapped["Habits"] = relationship("Habits", back_populates="habit_completions")

