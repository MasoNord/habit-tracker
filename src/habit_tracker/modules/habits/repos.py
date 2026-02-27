import datetime

from sqlalchemy import select, Sequence, delete, and_, literal, insert, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from habit_tracker.modules.habits.models import Habits, HabitLogs, HabitCompletion


class HabitsRepo:
    def __init__(self, session: AsyncSession):
        self.__session=session

    async def save(self, habit: Habits):
        try:
            self.__session.add(habit)
            await self.__session.commit()
        except SQLAlchemyError as e:
            await self.__session.rollback()
            raise e

        return habit

    async def exists(self, title: str, user_id: int) -> bool:
        stmt = select(literal(1)).where(
            and_(
                Habits.title == title,
                Habits.user_id == user_id
            )
        )

        result = await self.__session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def get_all(self, user_id: int) -> Sequence[Habits]:
        stmt = select(Habits).where(Habits.user_id == user_id)

        try:
            records = await self.__session.execute(stmt)
            habits = records.scalars().unique().all()
        except SQLAlchemyError as e:
            await self.__session.rollback()
            raise e

        return habits

    async def get_by_id(self, habit_id: int) -> Habits:
        stmt = select(Habits).where(Habits.id == habit_id)

        try:
            records = await self.__session.execute(stmt)
            habit = records.scalar_one_or_none()
        except SQLAlchemyError as e:
            await self.__session.rollback()
            raise e

        return habit

    async def delete_by_id(self, habit_id: int):
        stmt = delete(Habits).where(Habits.id == habit_id)

        try:
            await self.__session.execute(stmt)
            await self.__session.commit()
        except SQLAlchemyError as e:
            await self.__session.rollback()
            raise e

    async def update(self, habit: Habits, data: dict):
        for key, value in data.items():
            if getattr(habit, key) and value:
                setattr(habit, key, value)

        try:
            await self.__session.commit()
        except SQLAlchemyError as e:
            await self.__session.rollback()
            raise e

        return habit

class HabitLogsRepo:
    def __init__(self, session: AsyncSession):
        self.__session=session

    async def log_habit(self, habit_id: int, log_date: datetime.date):
        stmt = insert(HabitLogs).values(habit_id=habit_id, log_date=log_date)

        try:
            await self.__session.execute(stmt)
            await self.__session.commit()
        except SQLAlchemyError as e:
            await self.__session.rollback()
            raise e

    async def count_habit_logs(self, habit_id: int, log_date: datetime.date):
        stmt = select(func.count().label("logs")).where(and_(HabitLogs.habit_id==habit_id, HabitLogs.log_date==log_date))

        record = await self.__session.execute(stmt)
        result = record.scalar_one_or_none()

        return result

class HabitCompletionRepo:
    def __init__(self, session: AsyncSession):
        self.__session=session

    async def save(self, habit: HabitCompletion):
        try:
            self.__session.add(habit)
            await self.__session.commit()
        except SQLAlchemyError as e:
            await self.__session.rollback()
            raise e

        return habit
