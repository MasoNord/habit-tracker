import logging

from fastapi import FastAPI, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from habit_tracker.config import settings


log = logging.getLogger(__name__)

class CSRFCheckerMiddleWare(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        target_http_methods = {"POST", "DELETE", "PUT", "PATCH"}
        excluded_paths = [
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/api/v1/auth/logout",
            "/openapi.json",
        ]

        env = settings.ENV

        if (
            env == "prod"
            and request.method in target_http_methods
            and request.url.path not in excluded_paths
        ):
            cookies = request.cookies
            headers = request.headers

            csrf_cookie = cookies.get("csrftoken")
            csrf_header = headers.get("X-CSRF-TOKEN")

            if not csrf_header or not csrf_cookie or csrf_header != csrf_cookie:
                log.info("Incorrect csrf token")
                raise HTTPException(401, "CSRF token is invalid ")

        return await call_next(request)

def init_middleware(app: FastAPI):
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY, max_age=settings.SESSION_MAX_AGE, https_only=True)
    app.add_middleware(CSRFCheckerMiddleWare)
