from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_session
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

engine = create_async_engine(settings.POSTGRES_URI, echo=True, future=True)
# SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
