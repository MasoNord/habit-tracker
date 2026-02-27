from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from habit_tracker.db.engine import get_db
from habit_tracker.users.services import UserService
from habit_tracker.users.repos import UserRepo


async def get_user_repo(session: AsyncSession = Depends(get_db)) -> UserRepo:
    return UserRepo(session=session)

async def get_user_service(user_repo: UserRepo = Depends(get_user_repo)) -> UserService:
    return UserService(user_repo=user_repo)