# Module 9 — Final Tests & Launch Checklist
*Kick the tires before you share your AI website. You’ll run functional, mobile, load, and “break‑it” tests; add minimal safety; and follow a clean launch checklist.*

## 1. Before You Begin
### Purpose
You’ll confirm your site works for other people, not just on your machine. We’ll test functionality, mobile access, simple load, resilience, and basic safety before you share the link.

### What You’ll Need
- Modules 1–8 completed (your site is reachable via Cloudflare or a custom domain)
- A phone (mobile data preferred) and a friend for external checks
- 30–60 minutes
- Difficulty: ★★☆

### Why This Matters
Most problems show up only when *someone else* tries your site: wrong ports, blocked routes, DNS misfires, slow responses, or missing error handling. This module catches those early.

## 2. Overview of Steps
1. Functional checks (health, chat, error handling).  
2. Mobile & external checks.  
3. Simple load test (low‑risk).  
4. Break‑it tests (timeouts, long prompts).  
5. Minimal safety & privacy.  
6. Launch checklist & rollback plan.

---

## 3. Step‑by‑Step Instructions

### Step 1 — Functional Checks
**Goal:** Verify core routes behave as expected.

#### Instructions
1. **Health route:**  
```bash
curl -s https://YOUR_DOMAIN/health
```
Expect a JSON status like `{ "status": "ok" }`.

2. **Generate route:** (tiny prompt)  
```bash
curl -s -X POST https://YOUR_DOMAIN/generate   -H "Content-Type: application/json"   -d '{"prompt":"Say hi in one short sentence."}'
```
Expect a JSON with a “response” string.

3. **Bad payload test:**  
Send malformed JSON and confirm you return a 422/400, not a crash.

#### Mini Success Moment
> ✔️ Your API handles normal and bad requests without falling over.

---

### Step 2 — Mobile & External Checks
**Goal:** Prove the site works off your network and on a phone.

#### Instructions
1. Turn **off Wi‑Fi** on your phone (use mobile data).  
2. Visit `https://YOUR_DOMAIN/static/index.html`.  
3. Send a simple prompt and confirm you get a response.  
4. Ask a friend in a different location to test the same.

#### Expected Result
The page loads quickly, and the first response arrives within ~10 seconds on a small model.

#### Mini Success Moment
> ✔️ External users can access your site securely.

---

### Step 3 — Simple Load Test (Gentle)
**Goal:** Simulate a handful of simultaneous users without hurting your machine.

#### Instructions (Python one‑liner: 10 quick requests)**
```bash
python3 - << 'PY'
import json, time, requests
URL = "https://YOUR_DOMAIN/generate"
ok = 0
for i in range(10):
    try:
        r = requests.post(URL, json={"prompt": f"Ping {i}: say 'ok'."}, timeout=30)
        if r.ok and "response" in r.json():
            ok += 1
    except Exception as e:
        print("Error:", e)
print("OK:", ok, "/ 10")
PY
```
**Expected:** Most or all should pass (`OK: 8–10 / 10`).

> If your machine is slow, try **5** requests instead of 10.

#### Notes
- This is **not** a stress test. It’s a sanity test.
- Close big apps (browser tabs, IDEs) to free CPU/RAM.

#### Mini Success Moment
> ✔️ Your service handles basic traffic without collapsing.

---

### Step 4 — Break‑It Tests (Resilience)
**Goal:** Ensure graceful failure and timeouts.

#### Instructions
1. **Very long prompt** (e.g., paste 3–5 paragraphs).  
   - Expect: slower response, but still returns JSON.  
2. **Empty prompt** (send `""`).  
   - Expect: 400/422 with a clear error message.  
3. **Rapid double‑click send** in UI.  
   - Expect: second send blocked while first is running (Module 7 already disables the button).  
4. **Stop your backend** while the tunnel stays up, then request `/generate`.  
   - Expect: a 5xx from the tunnel and a readable error (no crash logs).

#### Mini Success Moment
> ✔️ Your app fails safely and recovers cleanly.

---

### Step 5 — Minimal Safety & Privacy
**Goal:** Avoid foot‑guns before sharing publicly.

#### Recommendations
- **Rate‑limit** requests to `/generate` to prevent spam (simple: a per‑minute counter in memory).  
- **Input size cap**: Reject prompts larger than, say, **2000 characters** with a friendly message.  
- **Logging**: Log timestamps, route, and response time — avoid logging full prompts if privacy‑sensitive.  
- **CORS**: Keep UI and API on the same origin to avoid cross‑site requests.  
- **Kill‑switch**: Add an env var `ENABLE_PUBLIC=0/1` and block `/generate` if set to `0`.

#### Example: tiny rate‑limit (per IP, in‑memory)
```python
# Add near the top of app.py
import time
from fastapi import Request, HTTPException

RATE = {}  # ip -> [timestamps]
WINDOW = 60  # seconds
LIMIT = 10  # requests per window

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    if request.url.path == "/generate":
        ip = request.client.host
        now = time.time()
        RATE.setdefault(ip, [])
        RATE[ip] = [t for t in RATE[ip] if now - t < WINDOW]
        if len(RATE[ip]) >= LIMIT:
            raise HTTPException(status_code=429, detail="Too many requests, slow down.")
        RATE[ip].append(now)
    return await call_next(request)
```

---

## 4. Launch Checklist
- [ ] Health route returns **ok** over HTTPS  
- [ ] `/generate` works with small prompts  
- [ ] Mobile (cell data) can reach UI and API  
- [ ] Friend in another location confirms access  
- [ ] Basic load test passes (8/10 OK)  
- [ ] Input size capped; rate‑limit enabled (optional but recommended)  
- [ ] Logs show request time (no secrets)  
- [ ] `.env` not in Git; tokens kept out of code  
- [ ] “Kill‑switch” env var documented  
- [ ] README updated with how to start/stop

---

## 5. Rollback Plan (If Things Go Sideways)
- Be ready to **stop the tunnel**: `Ctrl+C` in the tunnel terminal or `systemctl stop cloudflared`.  
- Temporarily **disable `/generate`** if needed (check an `ENABLE_PUBLIC` flag).  
- Revert to a minimal non‑LLM app (Module 5) while you fix issues.  
- Keep a copy of your previous known‑good files (`git tag v0.1-live`).

---

## 6. Recap — What You Accomplished
- Verified your site externally and on mobile  
- Ran a gentle load test and resilience checks  
- Added minimal safety and privacy guards  
- Prepared a clean launch checklist and rollback plan

## 7. What’s Next
You’re live! From here, you can:  
- Upgrade to faster models, add personas/memory, or deploy to a small cloud VM.  
- Add authentication (Cloudflare Access with One‑Time PIN is easy).  
- Start a **project log** with performance notes and user feedback.
