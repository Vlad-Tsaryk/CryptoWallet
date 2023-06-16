import time

from celery import shared_task
from loguru import logger


@shared_task(name="create_task")
def create_task(name):
    time.sleep(10)
    logger.info(name)
    return True
