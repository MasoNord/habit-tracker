from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT
from habit_tracker.auth.dependencies import get_auth_service
from habit_tracker.auth.services import AuthService
from habit_tracker.dto import ResponseMessage
from habit_tracker.modules.habits.dependencies import get_habit_service
from habit_tracker.modules.habits.dto import CreateHabitRequest, HabitResponse, UpdateHabitRequest, HabitFilters
from habit_tracker.modules.habits.services import HabitsServices

habits_router = APIRouter()

@habits_router.post("/", response_model=HabitResponse, status_code=HTTP_201_CREATED)
async def create_habit(
    request_data: CreateHabitRequest,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
    habits_service: HabitsServices = Depends(get_habit_service)
):

    user = await auth_service.get_current_user(request)

    return await habits_service.create_habit(user, request_data)

@habits_router.get("/users/", response_model=List[HabitResponse], status_code=HTTP_200_OK)
async def get_user_habits(
    request: Request,
    filters: HabitFilters = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
    habits_service: HabitsServices = Depends(get_habit_service)
):

    today = date.today()

    current_day_of_month = today.day

    user = await auth_service.get_current_user(request)

    return await habits_service.get_all(user, current_day_of_month, filters)

@habits_router.put("/{habit_id:int}", response_model=HabitResponse, status_code=HTTP_200_OK)
async def update_habit(
    habit_id: int,
    request: Request,
    request_data: UpdateHabitRequest,
    auth_service: AuthService = Depends(get_auth_service),
    habits_service: HabitsServices = Depends(get_habit_service)
):

    await auth_service.get_current_user(request)

    return await habits_service.update_habit(habit_id, request_data)

@habits_router.delete("/{habit_id:int}", status_code=HTTP_204_NO_CONTENT)
async def delete_habit(
    habit_id: int,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
    habits_service: HabitsServices = Depends(get_habit_service)
):

    await auth_service.get_current_user(request)

    return await habits_service.delete_by_id(habit_id)

@habits_router.post("/log/{habit_id:int}", response_model=ResponseMessage, status_code=HTTP_201_CREATED)
async def log_habit(
    habit_id: int,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
    habits_service: HabitsServices = Depends(get_habit_service)
):
    await auth_service.get_current_user(request)

    return await habits_service.log_habit(habit_id)