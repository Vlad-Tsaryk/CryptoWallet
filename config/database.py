from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

engine: AsyncEngine = create_async_engine(settings.POSTGRES_URI, future=True)
async_session: AsyncSession = sessionmaker(  # noqa
    engine, expire_on_commit=False, class_=AsyncSession
)
Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:  # noqa
        yield session
