.PHONY: install dev lint format test clean

install:
	python -m pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload --port 8000

lint:
	ruff check . && black --check .

format:
	black . && ruff check . --fix

test:
	pytest -q --cov=app

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
