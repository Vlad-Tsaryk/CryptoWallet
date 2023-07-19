from loguru import logger
from propan import RabbitBroker
from propan.fastapi import RabbitRouter

from src.wallet.tasks import parse_eth_blocks

router: RabbitRouter = RabbitRouter("amqp://guest:guest@localhost:5672")
broker: RabbitBroker = router.broker


@broker.handle("block_parser", "exchange")
async def process_block(block_hash):
    parse_eth_blocks.delay(block_hash)
    logger.info(block_hash)


# @broker.handle("ibay_serv", "exchange")
# async def ibay_serv(block_hash):
#     parse_eth_blocks.delay(block_hash)
#     logger.info(block_hash)
