.PHONY: all install build run test clean lint

all: install build test

install:
	pip install django djangorestframework django-cors-headers drf-spectacular pytest pytest-django
	cd frontend && npm install

build:
	cd frontend && npm run build
	python backend/manage.py collectstatic --noinput || true

run:
	python main.py

test:
	pytest -v

clean:
	rm -rf frontend/dist .pytest_cache *.pyc
