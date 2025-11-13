# Module 12 — Logging & Metrics (Latency, Errors, Tokens)
*Measure what matters: response time, success/failure, and rough token counts — so you can compare models and catch problems early.*

## 1. Before You Begin
### Purpose
You’ll add structured logging and simple metrics to your FastAPI app. You’ll record **latency**, **status**, **prompt size**, and **approximate tokens** per request, and expose a `/metrics` endpoint for quick checks (and future Prometheus use).

### What You’ll Need
- Modules 1–11 completed
- A working FastAPI `/generate` endpoint
- 20–40 minutes
- Difficulty: ★★☆

### Why This Matters
If you don’t measure it, you can’t improve it. Logging + metrics turns guesswork into data: “Is this model slower? Which prompts error out? Did our last change help?”

---

## 2. Add a Minimal Metrics Store
Create a new file `metrics.py`:
```python
# metrics.py — tiny in-memory counters & histograms
import time, threading
from collections import defaultdict, deque

_lock = threading.Lock()

COUNTERS = defaultdict(int)
LATENCY_MS = deque(maxlen=2000)  # rolling window

def inc(name: str, value: int = 1):
    with _lock:
        COUNTERS[name] += value

def observe_latency(ms: float):
    with _lock:
        LATENCY_MS.append(ms)

def snapshot():
    with _lock:
        # Copy safely
        counters = dict(COUNTERS)
        lat = list(LATENCY_MS)
    p50 = percentile(lat, 50)
    p90 = percentile(lat, 90)
    p99 = percentile(lat, 99)
    return counters, {"count": len(lat), "p50_ms": p50, "p90_ms": p90, "p99_ms": p99}

def percentile(values, p):
    if not values:
        return 0.0
    values = sorted(values)
    k = int(round((p/100) * (len(values)-1)))
    return float(values[k])
```

---

## 3. Structured Logging (JSONL)
Append JSON lines to `logs/requests.jsonl` so you can analyze later with any tool.

Create folder:
```bash
mkdir -p logs
```

Add a helper `log_utils.py`:
```python
# log_utils.py — append JSON per request
import json, os, time
from typing import Dict, Any

LOG_PATH = os.getenv("LOG_PATH", "logs/requests.jsonl")

def log_event(event: Dict[str, Any]):
    event = dict(event)
    event["ts"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
```

---

## 4. Wire Metrics & Logging into FastAPI
Edit your `app.py`:
```python
import time, uuid
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from model_loader import make_generator
from metrics import inc, observe_latency, snapshot
from log_utils import log_event

load_dotenv()
app = FastAPI()

generate = make_generator()

class Prompt(BaseModel):
    prompt: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    counters, lat = snapshot()
    # Simple text format (Prometheus-friendly-ish)
    lines = []
    for k, v in counters.items():
        lines.append(f"yfa_counter{{name=\"{k}\"}} {v}")
    lines.append(f"yfa_latency_count {lat['count']}")
    lines.append(f"yfa_latency_p50_ms {lat['p50_ms']}")
    lines.append(f"yfa_latency_p90_ms {lat['p90_ms']}")
    lines.append(f"yfa_latency_p99_ms {lat['p99_ms']}")
    return "\n".join(lines)

@app.post("/generate")
def generate_route(p: Prompt, request: Request):
    start = time.time()
    req_id = str(uuid.uuid4())[:8]
    prompt = p.prompt or ""
    prompt_chars = len(prompt)

    inc("requests_total")
    if prompt_chars == 0:
        inc("requests_bad")
        raise HTTPException(status_code=400, detail="Empty prompt")

    try:
        text = generate(prompt)
        ok = True
        inc("requests_ok")
    except Exception as e:
        ok = False
        inc("requests_error")
        text = f"ERROR: {e}"

    ms = round((time.time() - start) * 1000, 2)
    observe_latency(ms)

    # Rough token estimates (very approximate)
    # 1 token ≈ 4 chars (English). Adjust if you care later.
    in_tokens = prompt_chars // 4
    out_tokens = len(text) // 4 if isinstance(text, str) else 0

    log_event({
        "id": req_id,
        "path": "/generate",
        "ok": ok,
        "status": 200 if ok else 500,
        "latency_ms": ms,
        "prompt_chars": prompt_chars,
        "in_tokens_approx": in_tokens,
        "out_tokens_approx": out_tokens,
        "client_ip": request.client.host,
    })

    if not ok:
        raise HTTPException(status_code=500, detail="Generation failed")

    return {"response": text, "latency_ms": ms, "id": req_id}
```

Notes:
- This keeps everything **in-process** and **file-based** — simple and portable.  
- For serious deployments, send logs to a real system (e.g., OpenTelemetry, Loki, ELK, CloudWatch).

---

## 5. Quick Tests
With your server running:
```bash
curl -s http://localhost:8000/metrics | sed -n '1,20p'
curl -s -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"prompt":"Say hi"}'
curl -s http://localhost:8000/metrics | sed -n '1,20p'
tail -n 3 logs/requests.jsonl
```

Expected:
- Metrics include non‑zero counters and latency percentiles.  
- Logs show JSON lines with `latency_ms`, `in_tokens_approx`, `out_tokens_approx`.

---

## 6. Optional: Prometheus Scrape
Point Prometheus at:
```
- job_name: 'your-first-ai'
  static_configs:
  - targets: ['localhost:8000']
```
Then chart `yfa_latency_p50_ms`, `yfa_latency_p90_ms`, and `yfa_counter{name="requests_error"}`.

---

## 7. Optional: Correlation IDs in Responses
We already return `"id": "<short-uuid>"` in `/generate`. Include this in UI logs if you add client-side logging, so you can match browser events to server logs.

---

## 8. Checkpoint
- `/metrics` returns counters and latency stats.  
- `/generate` responses include `latency_ms` and an `id`.  
- `logs/requests.jsonl` fills with JSON events.

> ✔️ If true, Module 12 is complete.

---

## 9. What’s Next
In **Module 13**, you’ll add **basic auth**: Cloudflare Access (One‑Time PIN / Google login) or a simple shared password to protect your public demo.
