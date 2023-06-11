from loguru import logger
from propan import RabbitBroker
from propan.fastapi import RabbitRouter

router: RabbitRouter = RabbitRouter("amqp://guest:guest@localhost:5672")
broker: RabbitBroker = router.broker


@broker.handle("test")
async def test(m):
    logger.info(m)
