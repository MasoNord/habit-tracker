from sqlalchemy import Integer, ForeignKey, Date
from sqlalchemy.orm import mapped_column, Mapped, relationship
import datetime

from habit_tracker.db import Base
from habit_tracker.db.mixins import TimeStampMixin


class Pomodoros(Base, TimeStampMixin):
    __tablename__ = "pomodoros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["Users"] = relationship("Users", back_populates="pomodoros")
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"), nullable=True)
    habit: Mapped["Habits"] = relationship("Habits", back_populates="pomodoros")
    time_elapsed: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
