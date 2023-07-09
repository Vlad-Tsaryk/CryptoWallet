import asyncio

from celery import shared_task
from loguru import logger

from config.database import async_session
from config.web3 import get_web3
from src.wallet.service import get_all_wallets_address


async def get_addresses() -> list:
    async with async_session() as session:
        addresses = await get_all_wallets_address(session)
    return addresses


@shared_task(bind=True)
def parse_eth_blocks(self, reply):
    if reply:
        parse_eth_blocks.apply_async(countdown=12, kwargs={"reply": True})
    loop = asyncio.get_event_loop()
    addresses = loop.run_until_complete(get_addresses())
    logger.info(addresses)
    w3 = get_web3()
    block = w3.eth.get_block("latest", True)
    logger.info(block.get("number"))
    for transaction in block.get("transactions"):
        if transaction.get("to") in addresses or transaction.get("from") in addresses:
            logger.info(transaction)
            logger.info(transaction["s"].hex())
    return True
