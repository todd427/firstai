# Module 13 — Lightweight Auth for Your Public Demo
*Put a simple lock on your site so only the right people can try it. Two paths: (A) Cloudflare Access (One‑Time PIN / Google login) or (B) a shared password in FastAPI.*

## 1. Before You Begin
### Purpose
You’ll add a minimal authentication layer so your public demo isn’t open to the whole internet. Choose **Cloudflare Access** for a polished login flow, or use a **shared password** inside FastAPI.

### What You’ll Need
- Modules 1–12 completed
- A Cloudflare account and active Tunnel (for Path A)
- Your FastAPI app running (for Path B)
- 20–45 minutes
- Difficulty: ★★☆

### Why This Matters
Even simple auth prevents crawlers, spam, and accidental exposure. It also protects your rate‑limited `/generate` endpoint from casual abuse.

---

## 2. Path A — Cloudflare Access (Recommended)
Cloudflare Access sits **in front** of your tunnel. Users see a branded login page and verify via **One‑Time PIN** or **Google/Microsoft**.

### Step A1 — Create an Access Application
1. Open **Cloudflare Dashboard → Zero Trust** (may require enabling it on first use).  
2. Go to **Access → Applications → Add an application**.  
3. **Type:** Self‑hosted.  
4. **Name:** `Your First AI (Demo)`  
5. **Session duration:** e.g., `24 hours`.  
6. **Application domain:** your public hostname (e.g., `ai.yourdomain.com`).

### Step A2 — Set Policies
1. Create a policy named **Allow Trusted**:  
   - **Action:** Allow  
   - **Include:** Emails (add your email), or **Emails ending in** (e.g., your school domain), or **Any valid user** (for OTP).  
2. (Optional) Add a policy named **Block All Else**.  
3. Save.

### Step A3 — Choose Identity Providers
- **One‑Time PIN** (no configuration: users receive an email code).  
- **Google / Microsoft / GitHub** (click **Add** and follow prompts).

### Step A4 — Test the Flow
- Visit `https://ai.yourdomain.com/static/index.html`.  
- You should see the Access login page.  
- After passing, your app works normally.

> Pros: no code changes, easy policy control, logs of who accessed the app.  
> Cons: requires Cloudflare Zero Trust setup (still free for small usage).

---

## 3. Path B — Shared Password in FastAPI (Simple Lock)
Use a single password for **everyone** you share the link with. Not fancy, but fast.

### Step B1 — Add `.env` Secrets
Add to your `.env` (Module 3):
```
ENABLE_PUBLIC=1
DEMO_PASSWORD=change-me-please
```
Ensure `.env` is in `.gitignore`.

### Step B2 — Add a Middleware Gate
Edit `app.py` and add this near the top:
```python
import os
from fastapi import Request, HTTPException

ENABLE_PUBLIC = os.getenv("ENABLE_PUBLIC", "1") == "1"
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "")

PUBLIC_PATHS = {"/health", "/metrics", "/static/index.html", "/static"}

@app.middleware("http")
async def shared_password_gate(request: Request, call_next):
    # Allow basic assets and health without password
    path = request.url.path
    if any(path == p or path.startswith(p + "/") for p in PUBLIC_PATHS):
        return await call_next(request)

    if not ENABLE_PUBLIC:
        raise HTTPException(status_code=403, detail="Public access disabled by admin.")

    # Expect header: X-Demo-Password: <password>
    supplied = request.headers.get("X-Demo-Password", "")
    if DEMO_PASSWORD and supplied == DEMO_PASSWORD:
        return await call_next(request)

    raise HTTPException(status_code=401, detail="Missing or wrong demo password.")
```

### Step B3 — Client Update (Minimal)
In `static/index.html`, add a header when calling `/generate`.  
Find the `fetch` call and change to:
```js
const headers = {
  "Content-Type": "application/json",
  "X-Demo-Password": localStorage.getItem("demo_pw") || ""
};
```
And add a tiny prompt the first time:
```js
if (!localStorage.getItem("demo_pw")) {
  const pw = prompt("Enter demo password:");
  if (pw) localStorage.setItem("demo_pw", pw);
}
```

> If you prefer not to touch the client, you can pass the header via cURL or a simple `fetch` wrapper, but the prompt keeps things easy for demos.

### Step B4 — Test
- Restart your server and load the chat page.  
- You should be prompted for a password once per browser.  
- Requests to non‑public paths without the header should return **401**.

> Pros: dead simple, no third‑party setup.  
> Cons: All users share one password; no audit trail; not strong security.

---

## 4. Pick One (Or Combine)
- **Cloudflare Access** for real visitors, plus **shared password** for local/dev.  
- You can keep `ENABLE_PUBLIC=0` when you want to shut the gate instantly.

---

## 5. Checkpoint
- Path A: Cloudflare Access login appears and allows only approved users.  
- Path B: Shared password gate returns 401 without header and allows with correct header.  
- Your `/health` and `/metrics` remain reachable (or gated, your choice).

> ✔️ If true, Module 13 is complete.

---

## 6. What’s Next
In **Module 14**, you’ll package your project for others: a clean **README**, `requirements.txt`, `.env.example`, and a tiny **Makefile** so newcomers can run everything with two commands.
