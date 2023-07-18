start:
	uvicorn config_fastapi.app:app --reload
makemigrations:
	alembic revision -m "$(m)" --autogenerate
migrate:
	alembic upgrade head

celery_start:
	celery -A config_celery.celery worker --loglevel=info

start_block_pars:
	python3 blockchain_ws_service/parser.py
