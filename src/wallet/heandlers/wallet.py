from loguru import logger

from config_fastapi.broker import broker


@broker.handle("test")
async def test(m):
    logger.info(m)
