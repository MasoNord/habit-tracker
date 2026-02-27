import datetime
from typing import List

from fastapi import HTTPException
from datetime import date
from habit_tracker.dto import ResponseMessage
from habit_tracker.modules.habits.dto import CreateHabitRequest, HabitResponse, UpdateHabitRequest, HabitFilters
from habit_tracker.modules.habits.models import Habits, HabitCompletion
from habit_tracker.modules.habits.repos import HabitsRepo, HabitLogsRepo, HabitCompletionRepo
from habit_tracker.users.models import Users


class HabitsServices:
    def __init__(
        self,
        habits_repo: HabitsRepo,
        habit_logs_repo: HabitLogsRepo,
        habit_completion_repo: HabitCompletionRepo
    ):
        self.__habits_repo=habits_repo
        self.__habit_logs_repo=habit_logs_repo
        self.__habit_completion_repo=habit_completion_repo

    async def create_habit(self, user: Users, request_data: CreateHabitRequest) -> HabitResponse:

        if await self.__habits_repo.exists(request_data.title, user.id):
            raise HTTPException(409, "Habit with given name is already exists")

        habit = Habits(
            color=request_data.color,
            days_to_log=request_data.days_to_log,
            logs_to_complete=request_data.logs_to_complete,
            title=request_data.title,
            description=request_data.description,
            type=request_data.type.value,
            icon_url=request_data.icon_url,
            user_id=user.id
        )

        await self.__habits_repo.save(habit)

        return HabitResponse.model_validate(habit)

    async def get_all(self, user: Users, current_day: int, filters: HabitFilters) -> List[HabitResponse]:
        habits = await self.__habits_repo.get_all(user.id)

        response = []

        for h in habits:
            current_date = datetime.date.today()
            habit_current_log = await self.__habit_logs_repo.count_habit_logs(h.id, current_date)

            r = HabitResponse.model_validate(h)
            r.current_logs = habit_current_log

            if filters.tab == "today":
                if current_day in h.days_to_log:
                    response.append(r)
            elif filters.tab == "all":
                response.append(r)

        return response

    async def update_habit(self, habit_id, request_data: UpdateHabitRequest) -> HabitResponse:
        habit = await self.__habits_repo.get_by_id(habit_id)

        if not habit:
            raise HTTPException(404, "Habit not found")

        updated_habit = await self.__habits_repo.update(habit, request_data.model_dump())

        return HabitResponse.model_validate(updated_habit)

    async def delete_by_id(self, habit_id: int):
        habit = await self.__habits_repo.get_by_id(habit_id)

        if not habit:
            raise HTTPException(404, "Habit not found")

        await self.__habits_repo.delete_by_id(habit_id)

    async def log_habit(self, habit_id: int) -> ResponseMessage:
        habit = await self.__habits_repo.get_by_id(habit_id)

        if not habit:
            raise HTTPException(404, "Habit not found")

        current_date = datetime.date.today()

        await self.__habit_logs_repo.log_habit(habit.id, current_date)

        count_logs = await self.__habit_logs_repo.count_habit_logs(habit.id, current_date)

        # If habit logs to complete equals to current date habit logs
        # Record current streak for a given habit
        if habit.logs_to_complete == count_logs:
            current_date = datetime.date.today()
            habit_complete = HabitCompletion(
                habit_id=habit.id,
                date=current_date
            )

            await self.__habit_completion_repo.save(habit_complete)

            current_streak = habit.current_streak
            if not current_streak:
                current_streak = 1
            else:
                current_streak += 1

            await self.__habits_repo.update(habit, {"current_streak": current_streak})


        return ResponseMessage(message="Habit logged in")