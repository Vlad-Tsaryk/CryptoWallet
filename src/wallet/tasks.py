from celery import shared_task
from loguru import logger
from web3 import Web3

from config.config import settings


@shared_task
def create_task(name: str):
    w3 = Web3(Web3.HTTPProvider(settings.QUICK_NODE_URL))
    logger.info(w3.eth.get_transaction_by_block("latest", 0))
    return name
