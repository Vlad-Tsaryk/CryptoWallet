import asyncio

import aiohttp
from propan import RabbitBroker
from propan.fastapi import RabbitRouter

from config.config import settings
from ibay_service.service import db_query_func, order_to_delivery

router: RabbitRouter = RabbitRouter(settings.RABBITMQ_URL)
broker: RabbitBroker = router.broker


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


@broker.handle("ibay_queue", "exchange")
async def ibay_service(order_id):
    is_success = await send_google_requests()
    await db_query_func(order_to_delivery, order_id, is_success)
