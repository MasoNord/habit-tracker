from typing import Optional

from pydantic import BaseModel

class PomodoroResponse(BaseModel):
    start_date: int
    habit_id: Optional[int] = None