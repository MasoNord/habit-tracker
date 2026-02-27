from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from habit_tracker.db.engine import get_db
from habit_tracker.modules.habits.repos import HabitsRepo, HabitLogsRepo, HabitCompletionRepo
from habit_tracker.modules.habits.services import HabitsServices


async def get_habit_repo(session: AsyncSession = Depends(get_db)) -> HabitsRepo:
    return HabitsRepo(session=session)

async def get_habit_completion_repo(session: AsyncSession = Depends(get_db)) -> HabitCompletionRepo:
    return HabitCompletionRepo(session=session)

async def get_habit_logs_repo(session: AsyncSession = Depends(get_db)) -> HabitLogsRepo:
    return HabitLogsRepo(session=session)

async def get_habit_service(habits_repo: HabitsRepo = Depends(get_habit_repo),
                            habit_logs_repo: HabitLogsRepo = Depends(get_habit_logs_repo),
                            habit_completion_repo: HabitCompletionRepo = Depends(get_habit_completion_repo)) -> HabitsServices:
    return HabitsServices(habits_repo=habits_repo, habit_logs_repo=habit_logs_repo, habit_completion_repo=habit_completion_repo)
