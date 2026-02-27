from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from habit_tracker.auth.repos import AuthRepo
from habit_tracker.auth.services import AuthService
from habit_tracker.db.engine import get_db
from habit_tracker.users.dependencies import get_user_repo
from habit_tracker.users.repos import UserRepo


async def get_auth_repo(session: AsyncSession = Depends(get_db))-> AuthRepo:
    return AuthRepo(session=session)

async def get_auth_service(
        auth_repo: AuthRepo = Depends(get_auth_repo),
        user_repo: UserRepo = Depends(get_user_repo)
) -> AuthService:
    return AuthService(auth_repo=auth_repo, user_repo=user_repo)