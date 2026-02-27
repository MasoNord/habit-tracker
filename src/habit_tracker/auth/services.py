import datetime
import hashlib
import logging
import secrets
from datetime import timezone, timedelta
from hmac import compare_digest
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from habit_tracker.auth.repos import AuthRepo
from habit_tracker.config import settings
from habit_tracker.users.dto import UserLoginRequest, UserRegisterRequest, UserLoginResponse, UserRegisterResponse, \
    UserLogoutResponse
from habit_tracker.users.models import Users, UserSession
from habit_tracker.users.repos import UserRepo

log = logging.getLogger(__name__)

class AuthService:
    def __init__(self, auth_repo: AuthRepo, user_repo: UserRepo):
        self.__auth_repo = auth_repo
        self.__user_repo = user_repo

    async def login_user(self, request: Request, response: Response, user_login_request: UserLoginRequest) -> UserLoginResponse:
        user = await self.__user_repo.find_by_username(user_login_request.username)

        if not user:
            raise HTTPException(401, "The user's account not found")

        if not self.__verify_password(user.password, user_login_request.password):
            raise HTTPException(401, "Entered wrong password, try again")

        session_token = request.cookies.get("session_token")

        if session_token:
            hashed_session = self.__hash_token(session_token)
            user_session = await self.__auth_repo.get_session(hashed_session.decode("utf-8"))

            if user_session:
                if user_session.expires_at > datetime.datetime.now(tz=timezone.utc):
                    return UserLoginResponse(message="User logged in")

                await self.__auth_repo.delete_session(
                    user_session.session_token,
                    user_session.user_id
                )

        session_token = secrets.token_urlsafe(64)
        expires_at = datetime.datetime.now(tz=timezone.utc) + timedelta(days=2)
        hashed_session_token = self.__hash_token(session_token)
        csrf_token = secrets.token_urlsafe(64)


        user_session = UserSession(
            user_id=user.id,
            session_token=hashed_session_token.decode("utf-8"),
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            expires_at=expires_at
        )

        await self.__auth_repo.create_session(user_session)

        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=True,
            samesite=settings.SAMESITE,
            path="/",
            max_age=settings.SESSION_MAX_AGE
        )

        response.set_cookie(
            key="csrftoken",
            value=csrf_token,
            httponly=False,
            secure=settings.COOKIE_SECURE,
            samesite=settings.SAMESITE,
            path="/"
        )

        return UserLoginResponse(message="User logged in")

    async def register_user(self, user_register_request: UserRegisterRequest) -> UserRegisterResponse:
        user = Users(
            username=user_register_request.username,
            password=user_register_request.password
        )

        if await self.__user_repo.find_by_username(user.username):
            raise HTTPException(409, "Given username is already taken")

        if user.password != user_register_request.password_repeat:
            raise HTTPException(409, "Passwords dont' match")

        user.password = self.__hash_password(user.password)

        await self.__user_repo.save(user)

        return UserRegisterResponse(message="User's account created successfully")

    async def get_current_user(self, request: Request) -> Users:
        session_token = request.cookies.get("session_token")

        if not session_token:
            log.info("Session not foud in cookies")
            raise HTTPException(401, "Invalid session")

        hashed_session = self.__hash_token(session_token)
        user_session = await self.__auth_repo.get_session(hashed_session.decode("utf-8"))

        if not user_session:
            log.info("Active user session not found")
            raise HTTPException(401,"No active session found")

        if user_session.expires_at < datetime.datetime.now(tz=timezone.utc):
            log.info("Current user session has expired")
            await self.__auth_repo.delete_session(user_session.session_token, user_session.user_id)
            raise HTTPException(401, "Session expired")

        user = await self.__user_repo.find_by_id(user_session.user_id)

        return user

    async def logout(self, request: Request, response: Response) -> UserLogoutResponse:
        session_token = request.cookies.get("session_token")

        if not session_token:
            raise HTTPException(401, "Invalid session")

        hashed_session = self.__hash_token(session_token)
        user_session = await self.__auth_repo.get_session(hashed_session.decode("utf-8"))

        if not user_session:
            raise HTTPException(401,"No active session found")

        await self.__auth_repo.delete_session(user_session.session_token, user_session.user_id)

        response.delete_cookie(
            key="session_token",
            httponly=True,
            secure=True,
            samesite="lax"
        )

        return UserLogoutResponse(message="User logged out successfully")

    def __hash_password(self, word: str) -> str:
        """Hash password by using argon2 hashing algorithm"""
        ph = PasswordHasher()

        hashed_word = ph.hash(word)

        return hashed_word

    def __verify_password(self, hashed_word: str, word: str) -> bool:
        """Verify word with a hashed one"""
        try:
            ph = PasswordHasher()
            return ph.verify(hashed_word, word)
        except VerifyMismatchError:
            return False

    def __hash_token(self, token: str) -> bytes:
        """Hashing tokens before storing them to database"""
        h = hashlib.blake2b(digest_size=settings.AUTH_SIZE, key=settings.SECRET_KEY.encode("utf-8"))
        h.update(token.encode("utf-8"))

        return h.hexdigest().encode("utf-8")

    def __verify_hash(self, cookie: str, sig: bytes) -> bool:
        good_sig = self.__hash_token(cookie)
        return compare_digest(good_sig, sig)