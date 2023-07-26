import asyncio

from celery import shared_task

from src.ibay.service import return_order_money
from src.utils import db_query_func


@shared_task(bind=True)
def return_order_money_task(self, order_info: dict):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(db_query_func(return_order_money, order_info))
    return True
