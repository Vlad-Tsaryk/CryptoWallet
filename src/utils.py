from propan import RabbitBroker

from config.config import settings
from config.database import async_session


async def db_query_func(func, *args, **kwargs):
    async with async_session() as session:  # noqa
        return await func(session=session, *args, **kwargs)


async def publish_message(*args, **kwargs):
    async with RabbitBroker(settings.RABBITMQ_URL) as broker:
        await broker.publish(*args, **kwargs)
