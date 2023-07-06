from celery import Celery
from loguru import logger

from config.config import settings

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

celery.autodiscover_tasks(["src.wallet"], related_name="tasks", force=True)


@celery.task(name="test_task")
def test_task(name: str):
    logger.info(name)
    return "True"
