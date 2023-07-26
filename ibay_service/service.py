import asyncio

import aiohttp
from loguru import logger
from propan import RabbitBroker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from config.config import settings
from ibay_service.decorators import add_session
from src.ibay.models import OrderStatusChoices, Order


async def publish_message(*args, **kwargs):
    async with RabbitBroker(settings.RABBITMQ_URL) as broker:
        await broker.publish(*args, **kwargs)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def send_google_requests(num_requests=1000):
    url = "https://www.google.com"
    try:
        async with aiohttp.ClientSession() as session:
            tasks = [fetch(session, url) for _ in range(num_requests)]
            return await asyncio.gather(*tasks)
    except:
        return False


@add_session
async def order_to_delivery(order_id: int, is_success_requests, session: AsyncSession):
    order = await session.get(Order, order_id)
    if is_success_requests:
        order.status = OrderStatusChoices.DELIVERY.value
    else:
        order.status = OrderStatusChoices.FAILED.value
    await session.commit()


@add_session
async def get_oldest_delivery_order(session: AsyncSession) -> Order | None:
    smtp = (
        select(Order)
        .where(Order.status == OrderStatusChoices.DELIVERY.value)
        .options(selectinload(Order.product))
        .order_by(Order.id.desc())
    )
    order = await session.scalar(smtp)
    return order


# @add_session
# async def order_return_money(order_id: int, session: AsyncSession):
#     order = await session.scalar(select(Order).where(Order.id == order_id)
#                                  .options(selectinload(Order.product)))
#     logger.success(order.product.wallet.address)


@add_session
async def update_order_status(
    order: Order, status: OrderStatusChoices, session: AsyncSession
):
    status_value = status.value
    order.status = status_value
    await session.commit()
    logger.success(f"Order {order.id} status updated to {status_value}")
    if status_value == OrderStatusChoices.FAILED.value:
        await publish_message(
            queue="order_failed",
            exchange="exchange",
            message={"order_id": order.id, "tnx_hash": order.tnx_hash},
        )
