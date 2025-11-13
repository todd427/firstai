# Foundation F3 — Python Tools
*45–75 minutes | Your everyday Python toolkit*

## Objectives
- Create and manage virtual environments
- Install packages with `pip` and `pipx`
- Know when to reach for Poetry, pyenv, and Jupyter
- Format, lint, and test like a pro

## Prerequisites
Module 2 (Python installed).

## 1) Virtual Environments
```bash
cd ~/projects && mkdir f3 && cd f3
python3 -m venv .venv
source .venv/bin/activate
python -V && which python
```

Deactivate any time with `deactivate`.

## 2) pip Essentials
```bash
pip install --upgrade pip
pip install fastapi uvicorn pytest httpx
pip freeze | sed -n '1,10p'
pip uninstall <pkg>
```

Pin for reproducibility:
```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```

## 3) pipx (CLI Apps, Isolated)
```bash
sudo apt -y install pipx || python3 -m pip install --user pipx
pipx ensurepath
pipx install black
pipx run cowsay "pipx keeps CLIs isolated"
```

## 4) Format & Lint
```bash
pipx install black ruff
black .
ruff check .
```

Optional `pre-commit`:
```bash
pipx install pre-commit
pre-commit sample-config > .pre-commit-config.yaml
pre-commit install
```

## 5) Testing Basics
```bash
pytest -q
pytest -q -k health       # run tests that match 'health'
pytest -q -vv --maxfail=1
```

Minimal test file:
```python
# test_demo.py
def test_math():
    assert 2 + 2 == 4
```

## 6) Jupyter Quickstart
```bash
pip install jupyterlab
jupyter lab  # opens in browser
```

## 7) pyenv (Optional, multiple Python versions)
```bash
# Install deps then pyenv (see pyenv docs for your OS)
pyenv install --list | head
pyenv install 3.12.6
pyenv virtualenv 3.12.6 f3-venv
pyenv local f3-venv
python -V
```

## 8) Poetry (Optional, dependency management + packaging)
```bash
pipx install poetry
poetry init --no-interaction
poetry add fastapi uvicorn
poetry run uvicorn app:app
```

## 9) Checkpoint
- You can create a venv, install packages, and run `pytest`.
- You formatted code with `black` and saw ruff warnings.
- Optional: launched JupyterLab successfully.

## Exercises
1. Build a tiny FastAPI app with `/hello` and test it with `pytest`.
2. Add `black` + `ruff` via pre‑commit and trigger them on commit.
3. Create a Poetry project and compare workflow vs pip + venv.

## Troubleshooting
- **Module not found** — activate the venv: `source .venv/bin/activate`.
- **Permission errors** — never use `sudo` inside a venv; reinstall in the venv.
- **Kernel mismatch in Jupyter** — install `ipykernel` in the venv and select it from the UI.
