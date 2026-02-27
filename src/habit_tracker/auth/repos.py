from sqlalchemy import select, and_, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from habit_tracker.users.models import UserSession


class AuthRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_session(self, user_session: UserSession):
        try:
            self.__session.add(user_session)
            await self.__session.commit()
        except SQLAlchemyError as e:
            await self.__session.rollback()

    async def get_session(self, session_token: str) -> UserSession:
        stmt = select(UserSession).where(
            and_(UserSession.session_token == session_token)
        )

        try:
            record = await self.__session.execute(stmt)
            session = record.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e

        return session

    async def delete_session(self, session_token: str, user_id: int) -> bool:
        try:
            stmt = delete(UserSession).where(and_(UserSession.session_token == session_token, UserSession.user_id == user_id))

            await self.__session.execute(stmt)
            await self.__session.commit()
        except SQLAlchemyError as e:
            await self.__session.rollback()
            raise e

        return True