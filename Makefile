start:
	uvicorn config_fastapi.app:app --reload
makemigrations:
	alembic revision -m "$(m)" --autogenerate
migrate:
	alembic upgrade head
