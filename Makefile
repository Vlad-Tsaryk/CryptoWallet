start:
	uvicorn src.main:app --reload
makemigrations:
	alembic revision -m "$(m)" --autogenerate
migrate:
	alembic upgrade head
