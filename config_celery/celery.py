from celery import Celery

from config.config import settings


def create_celery_app() -> Celery:
    celery = Celery(__name__)
    celery.conf.broker_url = settings.CELERY_BROKER_URL
    celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

    celery.autodiscover_tasks(["src.wallet"], related_name="tasks", force=True)
    return celery


celery_app = create_celery_app()
