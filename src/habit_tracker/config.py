from pydantic.v1 import BaseSettings

from habit_tracker.utils.helpers import get_root_path

class Settings(BaseSettings):
    APP_PORT: int = 5000
    APP_HOST: str = "localhost"
    AUTH_SIZE: int
    ENV: str

    RD_HOST: str
    RD_PORT: str
    RD_PASSWORD: str
    RD_USERNAME: str

    PST_USER: str
    PST_PASSWORD: str
    PST_DATABASE: str
    PST_PORT: str = 5432
    PST_HOST: str = "localhost"
    ECHO_ALCHEMY_LOGS: bool
    SECRET_KEY: str
    SALT: str
    SESSION_MAX_AGE: int
    COOKIE_SECURE: str
    SAMESITE: str

    def get_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.PST_USER}:{self.PST_PASSWORD}@{self.PST_HOST}:{self.PST_PORT}/{self.PST_DATABASE}"

    def get_redis_url(self) -> str:
        return f"redis://{self.RD_USERNAME}:{self.RD_PASSWORD}@{self.RD_HOST}:{self.RD_PORT}"

    class Config:
        env_file = get_root_path() / ".env"
        extra = "ignore"

settings = Settings()