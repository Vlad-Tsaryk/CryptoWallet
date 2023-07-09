from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

engine: AsyncEngine = create_async_engine(settings.POSTGRES_URI, future=True)
async_session: AsyncSession = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
Base = declarative_base()
