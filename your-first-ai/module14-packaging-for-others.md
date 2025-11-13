# Module 14 — Package It for Others (One‑Command Start)
*Bundle your project so a newcomer can run it with two commands. We’ll add a `requirements.txt`, `.env.example`, a tiny `Makefile`, and a `quickstart.sh`.*

## 1. Before You Begin
### Purpose
You’ll make your project friendly for students, interns, or colleagues. A clean install path prevents “it works on my machine” headaches.

### What You’ll Add
- **`requirements.txt`** — the Python dependencies
- **`.env.example`** — a template of environment variables
- **`Makefile`** — `make setup`, `make run`, `make test`, `make tunnel`
- **`quickstart.sh`** — a one‑shot script for Linux/WSL/macOS

> These files assume you’ve built Modules 5–13. Adjust paths if you’re placing them in a different repo layout.

---

## 2. `requirements.txt`
Keep it minimal and portable. GPU‑specific installs vary by machine, so we default to CPU‑friendly packages.
```
fastapi>=0.115
uvicorn[standard]>=0.30
pydantic>=2.9
python-dotenv>=1.0
pyyaml>=6.0
huggingface_hub>=0.24
requests>=2.32

# Backends (install both so users can swap in Module 11)
llama-cpp-python>=0.2
transformers>=4.44
accelerate>=0.34
# ⚠️ PyTorch (torch) wheels differ by platform/GPU.
# Recommend installing following Module 6 instructions (CPU or CUDA).
```

---

## 3. `.env.example`
Ship a template so secrets never land in Git.
```
# App toggles
ENABLE_PUBLIC=1
MODEL_CONFIG=config/config.yaml
BACKEND_OVERRIDE=

# Demo shared password (Module 13 - Path B)
DEMO_PASSWORD=change-me-please

# Tokens (Module 3)
HF_TOKEN=
GITHUB_PAT=

# Logging (Module 12)
LOG_PATH=logs/requests.jsonl
```

---

## 4. `Makefile`
Make common tasks one command away.
```makefile
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
```

---

## 5. `quickstart.sh`
For users who don’t like Makefiles. Works on Linux, WSL, and macOS.
```bash
#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-8000}"

if [ ! -d ".venv" ]; then
  echo "==> Creating virtualenv .venv"
  python3 -m venv .venv
fi

echo "==> Activating venv and installing requirements"
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
  echo "==> Creating .env from .env.example"
  cp .env.example .env
fi

echo "==> Starting uvicorn on port ${PORT}"
exec uvicorn app:app --reload --port "${PORT}"
```

Make it executable:
```bash
chmod +x quickstart.sh
```

---

## 6. Quickstart for New Users
**Option A — Makefile**
```bash
git clone <your-repo-url> your-first-ai
cd your-first-ai
make setup
make dev
# Visit http://localhost:8000/static/index.html
```

**Option B — Shell script**
```bash
git clone <your-repo-url> your-first-ai
cd your-first-ai
./quickstart.sh
```

---

## 7. Final Checklist for Packaging
- [ ] `requirements.txt` reflects your actual imports.  
- [ ] `.env.example` is present; `.env` is **git‑ignored**.  
- [ ] `Makefile` and/or `quickstart.sh` work on a clean machine.  
- [ ] README has a **two‑minute start** section.  
- [ ] Tag a release, e.g., `v0.1-starter`.

## 8. What’s Next
From here you can branch into specialized tracks: **Players**, **Cyber awareness (Cybersafe)**, **Your First AI — Teacher Edition**, or build your **Student Handbook PDF**.
