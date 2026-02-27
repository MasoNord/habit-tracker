from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from habit_tracker.users.models import Users


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def find_by_id(self, user_id: int) -> Users:
        stmt = select(Users).where(Users.id == user_id)

        try:
            record = await self.__session.execute(stmt)
            user = record.scalar_one_or_none()
        except SQLAlchemyError as e:
            await self.__session.rollback()
            raise e
        return user

    async def find_by_username(self, username: str) -> Users:
        stmt = select(Users).where(Users.username == username)

        try:
            record = await self.__session.execute(stmt)
            user = record.scalar_one_or_none()
        except SQLAlchemyError as e:
            await self.__session.rollback()
            raise e
        return user

    async def save(self, user: Users) -> bool:
        try:
            self.__session.add(user)
            await self.__session.commit()
        except SQLAlchemyError as e:
            await self.__session.rollback()
            raise e
        return True