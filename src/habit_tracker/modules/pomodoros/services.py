import datetime
import json
import logging
from datetime import timezone
from typing import Optional
from venv import logger

from fastapi import HTTPException
from habit_tracker.dto import ResponseMessage
from habit_tracker.modules.pomodoros.dto import PomodoroResponse
from habit_tracker.modules.pomodoros.models import Pomodoros
from habit_tracker.modules.pomodoros.repos import PomodoroRepo
from habit_tracker.users.models import Users
from redis.asyncio import Redis


log = logging.getLogger(__name__)

class PomodoroService:
    def __init__(self, pomodoro_repo: PomodoroRepo, redis_client: Redis):
        self.__pomodoro_repo = pomodoro_repo
        self.__redis_client=redis_client

    async def start_pomodoro(self, user: Users, habit_id: Optional[int]) -> PomodoroResponse:
        key = f"pomodoro:{user.id}"

        if await self.__redis_client.get(name=key):
            raise HTTPException(409, "User has unfinished pomodoro session")


        start_date = int(datetime.datetime.now(tz=timezone.utc).timestamp())

        value = {
            "start_date": start_date,
            "habit_id": habit_id
        }

        await self.__redis_client.set(name=key, value=json.dumps(value))

        return PomodoroResponse(start_date=start_date, habit_id=habit_id)

    async def end_pomodoro(self, user: Users) -> ResponseMessage:
        key = f"pomodoro:{user.id}"

        log.info(f"Ending pomodoro for user: {user.id}")

        current_pomodoro = await self.__redis_client.get(name=key)

        if not current_pomodoro:
            raise HTTPException(409, "User pomodoro session not found")

        pomodoro_response = PomodoroResponse.model_validate(json.loads(current_pomodoro))

        current_time = int(datetime.datetime.now(tz=timezone.utc).timestamp())
        current_date = datetime.date.today()
        time_elapsed = current_time - pomodoro_response.start_date

        log.info(f"Current time {current_time}")
        log.info(f"Current date {current_date}")
        log.info(f"Current time elapsed {time_elapsed}")

        pomodoro = Pomodoros(
            user_id = user.id,
            habit_id = pomodoro_response.habit_id,
            time_elapsed=time_elapsed,
            date=current_date
        )

        await self.__pomodoro_repo.save(pomodoro)
        await self.__redis_client.delete(key)

        log.info("Pomodoro ended")

        return ResponseMessage(message="Pomodoro timer has ended")


    async def current_pomodoro(self, user: Users) -> PomodoroResponse:
        key = f"pomodoro:{user.id}"

        current_pomodoro = await self.__redis_client.get(name=key)

        if not current_pomodoro:
            raise HTTPException(404, "User pomodoro session not found")

        return PomodoroResponse.model_validate(json.loads(current_pomodoro))