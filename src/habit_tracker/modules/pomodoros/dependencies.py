from fastapi import Depends
from habit_tracker.db.engine import get_db
from habit_tracker.extensions.dependencies import get_redis
from habit_tracker.modules.pomodoros.repos import PomodoroRepo
from habit_tracker.modules.pomodoros.services import PomodoroService
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


async def get_pomodoro_repo(session: AsyncSession = Depends(get_db)) -> PomodoroRepo:
    return PomodoroRepo(session=session)

async def get_pomodoro_service(pomodoro_repo: PomodoroRepo = Depends(get_pomodoro_repo), redis_client: Redis = Depends(get_redis)):
    return PomodoroService(pomodoro_repo=pomodoro_repo, redis_client=redis_client)