# Module 5 — Verify Your Repo Runs Locally (Non‑LLM Test)
*Prove your environment works before adding any AI model. We’ll run a tiny FastAPI app, a health check, and a basic test.*

## 1. Before You Begin
### Purpose
You’ll create (or use) a minimal FastAPI app with a **/health** route, run it locally, and confirm that dependencies, ports, and file structure work on your machine — **without** loading any LLM. This prevents hours of confusion later.

### What You’ll Need
- Modules 1–4 completed
- Python 3.10+ installed in WSL/Ubuntu
- 20–40 minutes
- Difficulty: ★★☆

### Why This Matters
Most errors come from environment or routing problems, not models. A clean non‑LLM test gives you confidence that “the pipes work.”

## 2. Overview of Steps
1. Create a project folder and virtual environment.  
2. Install FastAPI, Uvicorn, and pytest.  
3. Add a minimal FastAPI app with a **/health** route.  
4. Run the server and load http://localhost:8000/health.  
5. Write a tiny test and run it.  
6. Fix common issues (ports, venv, imports).

---

## 3. Step‑by‑Step Instructions

### Step 1 — Create a Project and Virtual Environment
**Goal:** Isolate dependencies so your system stays clean.  
**Why:** Virtual environments prevent version conflicts.

#### Instructions
```bash
# Choose a working directory (e.g., your home)
cd ~
mkdir -p my_ai_app && cd my_ai_app

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# (Optional) Upgrade pip
pip install --upgrade pip
```

#### Expected Result
Your prompt shows `(.venv)` — that means the venv is active.

#### Common Issues & Fixes
- **Command not found: python3** → Install Python (Module 2) or use `python` if that’s your alias.  
- **Permissions** → Avoid `sudo` with pip inside venvs; it’s not needed.

#### Mini Success Moment
> ✔️ You’re working inside an isolated environment like a pro.

---

### Step 2 — Install Dependencies
**Goal:** Add only what you need.  
**Why:** Minimalism reduces problems.

#### Instructions
```bash
pip install fastapi uvicorn pytest httpx
```

#### Expected Result
Packages install without errors.

#### Common Issues & Fixes
- **SSL errors** → Check system time/date; ensure `sudo apt update && sudo apt -y upgrade` from Module 2.  
- **Network issues** → Try again later; verify internet in WSL.

#### Mini Success Moment
> ✔️ Your tools are ready.

---

### Step 3 — Create a Minimal App
**Goal:** Add a health endpoint to verify routing and imports.  
**Why:** Simple, testable, and universal.

#### Instructions
Create `app.py` with the following content:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok", "message": "Your First AI — non‑LLM stack works."}
```

#### Expected Result
No syntax errors when you save the file.

#### Mini Success Moment
> ✔️ The app exists. Time to run it.

---

### Step 4 — Run the Server
**Goal:** Serve your app locally.  
**Why:** Proves your FastAPI + Uvicorn setup works.

#### Instructions
```bash
uvicorn app:app --reload --port 8000
```
Open a browser to:
```
http://localhost:8000/health
```

#### Expected Result
You see JSON like:
```json
{"status":"ok","message":"Your First AI — non‑LLM stack works."}
```

#### Common Issues & Fixes
- **Port already in use** → Use another port: `--port 8020`, then visit `http://localhost:8020/health`.  
- **ImportError: No module named fastapi** → You forgot to activate the venv: `source .venv/bin/activate`.  
- **Nothing loads** → Are you in WSL? Try `curl http://localhost:8000/health` in the terminal.

#### Mini Success Moment
> ✔️ Your backend runs locally. The pipes work.

---

### Step 5 — Add a Basic Test
**Goal:** Run one test so you know pytest is wired correctly.  
**Why:** Confidence for future modules.

#### Instructions
Create `test_app.py`:
```python
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"
    assert "Your First AI" in data.get("message", "")
```

Run tests:
```bash
pytest -q
```

#### Expected Result
Output should end with:
```
1 passed
```

#### Common Issues & Fixes
- **ImportError: No module named 'app'** → Ensure `test_app.py` is in the same folder as `app.py`.  
- **Pytest not found** → `pip install pytest httpx` (re‑install inside venv).

#### Mini Success Moment
> ✔️ Your test passed. You’re ready to add models later.

---

## 4. Checkpoint Test
- Virtual environment active (`(.venv)` shown).  
- `uvicorn app:app` serves `/health`.  
- `pytest` shows **1 passed**.

> ✔️ If true, Module 5 is complete.

## 5. Troubleshooting Guide
- **Venv not activating** → Use `source .venv/bin/activate`; on Windows PowerShell, `.\.venv\Scripts\Activate.ps1`.  
- **Port issues** → Pick a different port (`8020`, `8030`, etc.).  
- **Package conflicts** → Create a fresh venv: `deactivate && rm -rf .venv && python3 -m venv .venv && source .venv/bin/activate`.  
- **WSL networking quirks** → Try `curl` from the same WSL shell to isolate issues.

## 6. Recap — What You Accomplished
- Created a clean Python virtual environment  
- Installed FastAPI + Uvicorn + pytest  
- Ran a health endpoint locally  
- Passed a test that proves the stack works without any LLM

## 7. What’s Next
In **Module 6**, you’ll plug in a small local model and perform your first generation — now that everything else is verified.
