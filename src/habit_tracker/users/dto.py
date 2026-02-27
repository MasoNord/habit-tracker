from typing import Optional
from pydantic import BaseModel, ConfigDict

class UserLoginRequest(BaseModel):
    username: str
    password: str

class UserRegisterRequest(BaseModel):
    username: str
    password: str
    password_repeat: str

class UserLoginResponse(BaseModel):
    message: str

class UserRegisterResponse(BaseModel):
    message: str


class UserReadResponse(BaseModel):
    id: int
    username: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class UserLogoutResponse(BaseModel):
    message: str