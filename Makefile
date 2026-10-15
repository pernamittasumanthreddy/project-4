.PHONY: all install build run test clean

all: install build

install:
	python -m pip install -r requirements.txt
	cd frontend && npm install

build:
	cd frontend && npm run build

run:
	python main.py

test:
	cd backend && pytest -q
	cd frontend && npm run test

clean:
	python -c "import shutil, glob; [shutil.rmtree(p, ignore_errors=True) for p in glob.glob('**/__pycache__', recursive=True)]"
