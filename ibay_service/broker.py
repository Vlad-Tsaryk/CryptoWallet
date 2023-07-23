import asyncio

import aiohttp
from propan import RabbitBroker
from propan.fastapi import RabbitRouter

from config.config import settings
from config.database import async_session
from src.ibay.models import Order, OrderStatusChoices

router: RabbitRouter = RabbitRouter(settings.RABBITMQ_URL)
broker: RabbitBroker = router.broker


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def send_google_requests(num_requests=1000):
    url = "https://www.google.com"

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for _ in range(num_requests)]
        return await asyncio.gather(*tasks)


@broker.handle("ibay_queue", "exchange")
async def ibay_service(order_id):
    is_success = await send_google_requests()
    async with async_session() as session:
        order = await session.get(Order, order_id)
        if is_success:
            order.status = OrderStatusChoices.DELIVERY.value
        else:
            order.status = OrderStatusChoices.FAILED.value
        # await session.commit()
