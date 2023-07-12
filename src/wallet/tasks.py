import asyncio

from celery import shared_task
from loguru import logger

from config.database import async_session
from config.web3 import get_web3
from src.wallet.schemas.transaction_schemas import StatusEnum, TransactionCreateOrUpdate
from src.wallet.service import (
    get_all_wallets_address,
    multiple_update_or_create_transaction,
)


async def get_addresses() -> list:
    async with async_session() as session:
        addresses = await get_all_wallets_address(session)
    return addresses


async def transactions_to_db(transaction_list: [TransactionCreateOrUpdate]) -> None:
    async with async_session() as session:
        await multiple_update_or_create_transaction(transaction_list, session)


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
    transaction_list = []
    for transaction in block.get("transactions"):
        if transaction.get("to") in addresses or transaction.get("from") in addresses:
            tnx_hash = transaction.get("hash").hex()
            trans_receipt = w3.eth.get_transaction_receipt(tnx_hash)
            transaction_list.append(
                TransactionCreateOrUpdate(
                    tnx_hash=tnx_hash,
                    from_address=trans_receipt.get("from"),
                    to_address=trans_receipt.get("to"),
                    value=w3.from_wei(transaction.get("value"), "ether"),
                    tnx_fee=w3.from_wei(
                        trans_receipt.get("gasUsed")
                        * trans_receipt.get("effectiveGasPrice"),
                        "ether",
                    ),
                    status=StatusEnum.success
                    if trans_receipt.get("status")
                    else StatusEnum.failed,
                )
            )
    if transaction_list:
        loop.run_until_complete(transactions_to_db(transaction_list))
    return True
