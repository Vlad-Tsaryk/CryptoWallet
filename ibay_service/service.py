from sqlalchemy.ext.asyncio import AsyncSession

from config.database import async_session
from src.ibay.models import OrderStatusChoices, Order


async def db_query_func(func, *args, **kwargs):
    async with async_session() as session:  # noqa
        return await func(session=session, *args, **kwargs)


async def order_to_delivery(order_id: int, is_success_requests, session: AsyncSession):
    order = await session.get(Order, order_id)
    if is_success_requests:
        order.status = OrderStatusChoices.DELIVERY.value
    else:
        order.status = OrderStatusChoices.FAILED.value
    await session.commit()
