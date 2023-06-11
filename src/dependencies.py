from propan import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import async_session
from config_fastapi.broker import broker


async def get_session() -> AsyncSession:
    async with async_session() as session:  # noqa
        yield session


def get_broker() -> RabbitBroker:
    return broker


# async def get_broker() -> RabbitBroker:
#     async with app.router.broker as broker:  # noqa
#         await broker.start()
#         yield broker
#         await broker.close()
