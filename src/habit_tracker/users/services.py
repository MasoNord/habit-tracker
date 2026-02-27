from starlette.requests import Request
from starlette.responses import Response

from habit_tracker.users.models import Users
from habit_tracker.users.repos import UserRepo


class UserService:
    def __init__(
        self,
        user_repo: UserRepo,
    ):
        self.__user_repo = user_repo

