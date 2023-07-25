import asyncio
from typing import List

from celery import shared_task
from loguru import logger
from propan import RabbitBroker

from config.config import settings
from config.database import async_session
from config.web3 import get_web3
from src.ibay.service import multiple_order_update
from src.wallet.models import ParsedBlock
from src.wallet.schemas.transaction_schemas import StatusEnum, TransactionCreateOrUpdate
from src.wallet.service import (
    get_all_wallets_address,
    multiple_update_or_create_transaction,
    get_last_parsed_block,
)


async def db_query_func(func, *args, **kwargs):
    async with async_session() as session:
        return await func(session=session, *args, **kwargs)


async def get_addresses() -> list:
    return await db_query_func(get_all_wallets_address)


async def db_last_parsed_block() -> int:
    block = await db_query_func(get_last_parsed_block)
    return block.number


async def parsed_block_to_db(number: int):
    async with async_session() as session:
        session.add(ParsedBlock(number=number))
        await session.commit()
    return True


async def publish_message(*args, **kwargs):
    async with RabbitBroker(settings.RABBITMQ_URL) as broker:
        await broker.publish(*args, **kwargs)


async def add_broker_to_func(func, *args, **kwargs):
    async with RabbitBroker(settings.RABBITMQ_URL) as broker:
        await db_query_func(func, *args, **kwargs, broker=broker)
        # await broker.publish(*args, **kwargs)


def process_block_transactions(
    w3, block
) -> List[TransactionCreateOrUpdate] | List[None]:
    loop = asyncio.get_event_loop()
    addresses = loop.run_until_complete(get_addresses())
    transaction_list = []
    transaction_hash_list = []
    for transaction in block.get("transactions"):
        if transaction.get("to") in addresses or transaction.get("from") in addresses:
            tnx_hash = transaction.get("hash").hex()
            transaction_hash_list.append(tnx_hash)
            trans_receipt = w3.eth.get_transaction_receipt(tnx_hash)
            transaction_create_or_update = TransactionCreateOrUpdate(
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

            transaction_list.append(transaction_create_or_update)
    if transaction_hash_list:
        loop.run_until_complete(
            add_broker_to_func(multiple_order_update, transaction_hash_list)
        )
    return transaction_list


@shared_task(bind=True)
def test_task(self):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        publish_message(queue="ibay_queue", exchange="exchange", message=1)
    )
    logger.info("hi")
    return True


@shared_task(bind=True)
def parse_to_last_block(
    self, block_hash, current_block_number=None, latest_block_number=None
):
    loop = asyncio.get_event_loop()
    w3 = get_web3()
    if not current_block_number:
        current_block_number = loop.run_until_complete(db_last_parsed_block())
    if not latest_block_number:
        latest_block = w3.eth.get_block(block_hash)
        latest_block_number = latest_block.get("number")
        logger.success(
            f"Start parse from **{current_block_number}** to last block **{latest_block_number}**"
        )
    if latest_block_number != current_block_number:
        current_block_number += 1
        parse_to_last_block.delay(block_hash, current_block_number, latest_block_number)
        try:
            current_block = w3.eth.get_block(current_block_number, True)
        except Exception as e:
            loop.run_until_complete(asyncio.sleep(1))
            current_block = w3.eth.get_block(current_block_number, True)
        current_block_number = current_block.get("number")
        loop.run_until_complete(parsed_block_to_db(current_block_number))
        logger.success(f"Parse block {current_block_number}")
        transaction_list = process_block_transactions(w3, current_block)
        if transaction_list:
            loop.run_until_complete(
                db_query_func(multiple_update_or_create_transaction, transaction_list)
            )
    return True


@shared_task(bind=True)
def parse_eth_blocks(self, block_hash):
    loop = asyncio.get_event_loop()
    w3 = get_web3()
    block = w3.eth.get_block(block_hash, True)
    block_number = block.get("number")
    loop.run_until_complete(parsed_block_to_db(block_number))
    transaction_list = process_block_transactions(w3, block)
    if transaction_list:
        loop.run_until_complete(
            db_query_func(multiple_update_or_create_transaction, transaction_list)
        )
    logger.info(f"Block **{block_number}** parsed successfully")
    return True
