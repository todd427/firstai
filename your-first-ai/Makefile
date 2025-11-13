.PHONY: help setup install run dev test metrics tunnel clean

PY?=python3
PIP?=pip3
PORT?=8000

help:
	@echo "Targets:"
	@echo "  setup     Create venv and install requirements"
	@echo "  install   Install requirements into existing venv"
	@echo "  run       Run FastAPI (uvicorn) on PORT=$(PORT)"
	@echo "  dev       Run with auto-reload"
	@echo "  test      Quick health check and sample /generate call"
	@echo "  metrics   Show first lines of /metrics"
	@echo "  tunnel    Quick Cloudflare tunnel to localhost:$(PORT)"
	@echo "  clean     Remove .venv and __pycache__"

setup:
	$(PY) -m venv .venv && . .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@echo "➡ Activate with: source .venv/bin/activate"

install:
	. .venv/bin/activate && pip install -r requirements.txt

run:
	. .venv/bin/activate && uvicorn app:app --port $(PORT)

dev:
	. .venv/bin/activate && uvicorn app:app --reload --port $(PORT)

test:
	curl -s http://localhost:$(PORT)/health || true
	curl -s -X POST http://localhost:$(PORT)/generate -H "Content-Type: application/json" -d '{"prompt":"Say hi in a short sentence."}' || true

metrics:
	curl -s http://localhost:$(PORT)/metrics | sed -n '1,20p' || true

tunnel:
	cloudflared tunnel --url http://localhost:$(PORT)

clean:
	rm -rf .venv __pycache__ */__pycache__
