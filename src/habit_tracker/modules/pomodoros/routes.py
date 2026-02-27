from typing import Optional

from fastapi import APIRouter, Query, Depends
from habit_tracker.auth.dependencies import get_auth_service
from habit_tracker.auth.services import AuthService
from habit_tracker.dto import ResponseMessage
from habit_tracker.modules.pomodoros.dependencies import get_pomodoro_service
from habit_tracker.modules.pomodoros.dto import PomodoroResponse
from habit_tracker.modules.pomodoros.services import PomodoroService
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

pomodoro_router = APIRouter()


@pomodoro_router.post("/start", response_model=PomodoroResponse, status_code=HTTP_201_CREATED)
async def start_pomodoro(
        request: Request,
        habit_id: Optional[int] = Query(None),
        auth_service: AuthService = Depends(get_auth_service),
        pomodoro_service: PomodoroService = Depends(get_pomodoro_service)
):
    user = await auth_service.get_current_user(request)
    return await pomodoro_service.start_pomodoro(user, habit_id)


@pomodoro_router.post("/end", response_model=ResponseMessage, status_code=HTTP_200_OK)
async def end_pomodoro(
        request: Request,
        auth_service: AuthService = Depends(get_auth_service),
        pomodoro_service: PomodoroService = Depends(get_pomodoro_service)
):
    user = await auth_service.get_current_user(request)
    return await pomodoro_service.end_pomodoro(user)

@pomodoro_router.get("/current", response_model=PomodoroResponse, status_code=HTTP_200_OK)
async def get_current_pomodoro(
        request: Request,
        auth_service: AuthService = Depends(get_auth_service),
        pomodoro_service: PomodoroService = Depends(get_pomodoro_service)
):
    user = await auth_service.get_current_user(request)
    return await pomodoro_service.current_pomodoro(user)
