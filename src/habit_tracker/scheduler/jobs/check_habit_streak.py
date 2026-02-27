import datetime
import logging
from typing import Sequence

from sqlalchemy import select, update, desc
from sqlalchemy.exc import SQLAlchemyError

from habit_tracker.db.engine import AsyncSessionLocal
from habit_tracker.modules.habits.models import Habits, HabitCompletion

FORMAT_STRING = "%Y-%m-%d"
log = logging.getLogger(__name__)

async def get_habits() -> Sequence[Habits]:
    log.info("Started fetching all habits")
    async with AsyncSessionLocal() as session:
        stmt = select(Habits)

        record = await session.execute(stmt)
        results = record.scalars().unique().all()

        log.info("Ended fetching all habits")

    return results


async def get_last_habit_completion(habit_id: int) -> HabitCompletion:
    log.info(f"Started fetching habit completion for habit: {habit_id}")
    async with AsyncSessionLocal() as session:
        stmt = select(HabitCompletion).where(HabitCompletion.habit_id == habit_id).order_by(desc(HabitCompletion.date))
        record = await session.execute(stmt)
        result = record.scalar_one_or_none()

        log.info("Ended fetching habit completion")
        return result

async def invalidate_habit_streak(habit_id: int):
    async with AsyncSessionLocal() as session:
        current_date = datetime.date.today()
        stmt = update(Habits).values(current_streak=0, last_completed_date=current_date).where(Habits.id==habit_id)
        try:
            await session.execute(stmt)
            await session.commit()
        except SQLAlchemyError as e:
            log.info("Error occurred while invalidating habit streak: {e}")
            session.rollback()

async def check_habit_streak():
    habits = await get_habits()

    current_date = datetime.date.today()
    for h in habits:
        habit_completion = await get_last_habit_completion(h.id)
        if habit_completion and h.current_streak != 0:
            diff = current_date - habit_completion.date

            if diff.days > 1:
                log.info(f"Invalidating log streak for habit: {h.id}")
                await invalidate_habit_streak(h.id)

async def wrapper():
    await check_habit_streak()


