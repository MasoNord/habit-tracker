from fastapi import APIRouter, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from habit_tracker.auth.dependencies import get_auth_service
from habit_tracker.auth.services import AuthService
from habit_tracker.users.dto import UserLoginResponse, UserRegisterResponse, UserReadResponse, UserLoginRequest, \
    UserRegisterRequest, UserLogoutResponse

auth_router = APIRouter()


@auth_router.post("/login", response_model=UserLoginResponse, status_code=status.HTTP_200_OK)
async def login(
        request_data: UserLoginRequest,
        request: Request,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service)):

    return await auth_service.login_user(request=request, response=response, user_login_request=request_data)


@auth_router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(request_data: UserRegisterRequest, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.register_user(request_data)


@auth_router.get("/me", response_model=UserReadResponse, status_code=status.HTTP_200_OK)
async def get_me(request: Request, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.get_current_user(request)

@auth_router.post("/logout", response_model=UserLogoutResponse, status_code=status.HTTP_200_OK)
async def user_logout(request: Request, response: Response, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.logout(request, response)

