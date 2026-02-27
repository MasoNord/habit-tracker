from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc


jobstores = {
    'default': MemoryJobStore()
}
executors = {
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': True,
    'max_instances': 3
}
scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
