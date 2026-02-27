from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status

helper_router = APIRouter()

class PingResponse(BaseModel):
    message: str

@helper_router.get("/", response_model=PingResponse, status_code=status.HTTP_200_OK)
async def ping() -> PingResponse:
    return  PingResponse(message="Pong!")
