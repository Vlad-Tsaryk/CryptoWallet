from loguru import logger
from propan.fastapi import RabbitRouter

from config.config import settings

router: RabbitRouter = RabbitRouter(settings.RABBITMQ_URL)


@router.event("block_parser", exchange="exchange")
async def process_block(block_hash):
    from src.wallet.tasks import parse_eth_blocks

    parse_eth_blocks.delay(block_hash)
    logger.info(block_hash)


@router.event("to_last_block", exchange="exchange")
async def to_last_block(block_hash):
    from src.wallet.tasks import parse_to_last_block

    parse_to_last_block.delay(block_hash)
    logger.info(block_hash)
