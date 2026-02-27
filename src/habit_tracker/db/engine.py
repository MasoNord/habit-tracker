from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.sql.schema import MetaData
from habit_tracker.config import settings

metadata = MetaData()

async_engine = create_async_engine(url=settings.get_db_url(), echo=settings.ECHO_ALCHEMY_LOGS)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        await session.close()
