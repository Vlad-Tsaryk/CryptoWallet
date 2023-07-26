import asyncio
import random

from loguru import logger

from ibay_service.service import (
    get_oldest_delivery_order,
    update_order_status,
    OrderStatusChoices,
)


async def start_delivery_service():
    logger.info("Start delivery service")
    while True:
        order = await get_oldest_delivery_order()
        logger.success(order)
        if order:
            status = OrderStatusChoices.FAILED
            if bool(random.getrandbits(1)):
                status = OrderStatusChoices.SUCCESS
            await update_order_status(order, status)
        await asyncio.sleep(5)
