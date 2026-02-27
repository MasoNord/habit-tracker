from enum import StrEnum
from typing import Optional, Self

from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict, model_validator

from habit_tracker.dto import BaseFilter


class HabitType(StrEnum):
    GOOD = "good"
    BAD = "bad"

class HabitStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    MISSED = "missed"


class HabitResponse(BaseModel):
    id: int
    description: Optional[str] = None
    current_logs: Optional[int] = 0
    title: str
    color: str
    days_to_log: list[int]
    logs_to_complete: int
    type: str
    icon_url: str

    model_config = ConfigDict(from_attributes=True)

class CreateHabitRequest(BaseModel):
    title: str = Field(max_length=256)
    color: str = Field(max_length=125)
    description: Optional[str] = None
    days_to_log: list[int]
    type: HabitType
    icon_url: str
    logs_to_complete: int

    @model_validator(mode="after")
    def check_days_to_log(self) -> Self:
        valid_days = {0, 1, 2, 3, 4, 5, 6}
        if not set(self.days_to_log).issubset(valid_days):
            raise ValueError("Unsupported values passed to valid_days")

        return self

class UpdateHabitRequest(BaseModel):
    title: Optional[str] = Field(max_length=256, default=None)
    description: Optional[str] = None
    icon_url: Optional[str] = None


class HabitFilters(BaseFilter):
    tab: Optional[str] = Query("all")