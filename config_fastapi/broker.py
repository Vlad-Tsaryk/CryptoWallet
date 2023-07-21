from loguru import logger
from propan import RabbitBroker
from propan.fastapi import RabbitRouter

from config.config import settings
from src.wallet.tasks import parse_eth_blocks, parse_to_last_block

router: RabbitRouter = RabbitRouter(settings.RABBITMQ_URL)
broker: RabbitBroker = router.broker


@broker.handle("block_parser", "exchange")
async def process_block(block_hash):
    parse_eth_blocks.delay(block_hash)
    logger.info(block_hash)


@broker.handle("to_last_block", "exchange")
async def to_last_block(block_hash):
    parse_to_last_block.delay(block_hash)
    logger.info(block_hash)
