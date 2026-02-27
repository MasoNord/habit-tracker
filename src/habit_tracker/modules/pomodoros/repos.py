from habit_tracker.modules.pomodoros.models import Pomodoros
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

class PomodoroRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def save(self, pomodoro: Pomodoros):
        try:
            self.__session.add(pomodoro)
            await self.__session.commit()
        except SQLAlchemyError as e:
            await self.__session.rollback()
            raise e