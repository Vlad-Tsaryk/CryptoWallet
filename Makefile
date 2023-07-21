start:
	uvicorn config_fastapi.app:app --reload
makemigrations:
	alembic revision -m "$(m)" --autogenerate
migrate:
	alembic upgrade head

celery_start:
	celery -A config_celery.celery worker --loglevel=info

blockchain_parser_start:
	propan run blockchain_ws_service.parser:app
