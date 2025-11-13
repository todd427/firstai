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
