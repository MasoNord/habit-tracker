import logging
from contextlib import asynccontextmanager

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI

from habit_tracker.cors import init_cors
from habit_tracker.extensions.redis import redis_client
from habit_tracker.logs import configure_logging
from habit_tracker.middlewares import init_middleware
from habit_tracker.routes import init_routers
from habit_tracker.scheduler.jobs.check_habit_streak import check_habit_streak, wrapper
from habit_tracker.scheduler.setup import scheduler

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_client.connect()
    log.info("Connection to redis...")

    scheduler.start()
    scheduler.add_job(wrapper, coalesce=True, trigger=IntervalTrigger(seconds=10))

    yield

    log.info("Disconnecting from redis...")
    await redis_client.close()

def create_app() -> FastAPI:
    app = FastAPI(
        title="API v1",
        description="The first version of the Habit Tracker APP",
        lifespan=lifespan
    )
    configure_logging()
    init_cors(app)
    init_routers(app)
    init_middleware(app)

    return app
