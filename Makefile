.PHONY: install dev test lint run demo clean

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src tests

run:
	uvicorn gateway.main:app --reload --port 8000

demo: install
	python -m gateway.demo

clean:
	rm -rf .pytest_cache .ruff_cache **/__pycache__
