from loguru import logger
from propan.fastapi import RabbitRouter

from config.config import settings
from src.ibay.tasks import return_order_money_task
from src.wallet.tasks import parse_eth_blocks, parse_to_last_block

router: RabbitRouter = RabbitRouter(settings.RABBITMQ_URL)


@router.event("block_parser", exchange="exchange")
async def process_block(block_hash):
    parse_eth_blocks.delay(block_hash)
    logger.info(block_hash)


@router.event("to_last_block", exchange="exchange")
async def to_last_block(block_hash):
    parse_to_last_block.delay(block_hash)
    logger.info(block_hash)


@router.event("order_failed", exchange="exchange")
async def to_last_block(order_info: dict):
    return_order_money_task.delay(order_info)
    logger.info(order_info)
