from fastapi import APIRouter, FastAPI

from habit_tracker.auth.routes import auth_router
from habit_tracker.modules.habits.routes import habits_router
from habit_tracker.modules.helper.routes import helper_router
from habit_tracker.modules.pomodoros.routes import pomodoro_router

API_VERSION = '/api/v1'

root_router = APIRouter()

root_router.include_router(
    helper_router,
    prefix=f"{API_VERSION}",
    tags=["Helper route"]
)

root_router.include_router(
    auth_router,
    prefix=f"{API_VERSION}/auth",
    tags=["Auth route"]
)

root_router.include_router(
    habits_router,
    prefix=f"{API_VERSION}/habits",
    tags=["Habits route"]
)

root_router.include_router(
    pomodoro_router,
    prefix=f"{API_VERSION}/pomodoros",
    tags=["Pomodoro route"]
)

def init_routers(app: FastAPI):
    app.include_router(root_router)