from propan.fastapi import RabbitRouter

from config.config import settings
from ibay_service.service import order_to_delivery, send_google_requests

router: RabbitRouter = RabbitRouter(settings.RABBITMQ_URL)


@router.event("ibay_delivery", exchange="exchange")
async def ibay_delivery(order_id):
    is_success = await send_google_requests()
    await order_to_delivery(order_id, is_success)
