# Module 7 — Local Web UI (Browser Chat to `/generate`)
*Build a simple HTML/JS page that talks to your FastAPI `/generate` endpoint. You’ll chat with your local model in a browser.*

## 1. Before You Begin
### Purpose
You’ll create a minimal web interface that sends a prompt to your existing `/generate` API (from Module 6) and displays the model’s response.

### What You’ll Need
- Modules 1–6 complete
- A running FastAPI app that exposes `POST /generate`
- 20–40 minutes
- Difficulty: ★★☆

### Why This Matters
Seeing a browser UI turns your local model into a mini‑app. It also sets you up for public sharing in later modules.

## 2. Overview of Steps
1. Create `static/index.html` (chat UI).  
2. (FastAPI) Serve the `static/` folder.  
3. Test the UI locally.  
4. Add simple UX improvements (enter‑to‑send, disabled button, scroll).  
5. Troubleshoot CORS/route issues if needed.

---

## 3. Step‑by‑Step Instructions

### Step 1 — Create the Chat Page
**Goal:** A single HTML file that sends prompts to `/generate` and shows replies.

#### Instructions
Create folders and the page:
```bash
mkdir -p static
nano static/index.html
```

Paste this:
```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Your First AI — Local Chat</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 0; background:#fafafa; }
    header { background:#111; color:#fff; padding:12px 16px; }
    main { max-width: 900px; margin: 0 auto; padding: 16px; }
    #log { background:#fff; border:1px solid #ddd; border-radius:8px; padding:16px; height: 60vh; overflow:auto; }
    .msg { margin: 10px 0; }
    .user { font-weight:600; }
    .ai { white-space: pre-wrap; }
    form { display:flex; gap:8px; margin-top:12px; }
    input, button, textarea { font-size: 16px; }
    textarea { flex:1; resize: vertical; min-height: 44px; }
    button { padding: 10px 14px; cursor: pointer; }
    .muted { color:#666; font-size: 14px; }
  </style>
</head>
<body>
  <header><strong>Your First AI</strong> — Local Chat</header>
  <main>
    <div id="log" aria-live="polite" aria-busy="false"></div>
    <form id="chat">
      <textarea id="prompt" placeholder="Type your message…" autofocus></textarea>
      <button id="send" type="submit">Send</button>
    </form>
    <p class="muted">This UI posts to <code>/generate</code> on the same server. Keep your FastAPI app running.</p>
  </main>

  <script>
    const form = document.getElementById('chat');
    const input = document.getElementById('prompt');
    const sendBtn = document.getElementById('send');
    const log = document.getElementById('log');

    function addLine(role, text){
      const div = document.createElement('div');
      div.className = 'msg ' + role;
      div.textContent = (role === 'user' ? 'You: ' : 'AI: ') + text;
      log.appendChild(div);
      log.scrollTop = log.scrollHeight;
    }

    async function ask(prompt){
      const url = '/generate';
      const body = JSON.stringify({ prompt });
      const headers = { 'Content-Type': 'application/json' };
      try {
        const r = await fetch(url, { method:'POST', headers, body });
        if(!r.ok){
          const t = await r.text();
          throw new Error('HTTP ' + r.status + ': ' + t);
        }
        const data = await r.json();
        return data.response || data.text || JSON.stringify(data);
      } catch (e){
        return 'Error: ' + e.message;
      }
    }

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const q = input.value.trim();
      if(!q) return;
      addLine('user', q);
      input.value = '';
      input.disabled = true;
      sendBtn.disabled = true;
      log.setAttribute('aria-busy', 'true');
      const a = await ask(q);
      log.setAttribute('aria-busy', 'false');
      addLine('ai', a);
      input.disabled = false;
      sendBtn.disabled = false;
      input.focus();
    });

    // Press Enter to send (Shift+Enter for newline)
    input.addEventListener('keydown', (e) => {
      if(e.key === 'Enter' && !e.shiftKey){
        e.preventDefault();
        sendBtn.click();
      }
    });
  </script>
</body>
</html>
```

#### Expected Result
A clean chat page with a message log and input box.

#### Mini Success Moment
> ✔️ You’ve got a local chat UI.

---

### Step 2 — Serve `static/` via FastAPI
**Goal:** Make `/` serve your chat page.  
**Why:** So your UI and API are on the same origin (no CORS headaches).

#### Instructions
Edit your `app.py` to mount static files:
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# If you followed Module 6 (llama-cpp or transformers), keep that code.
# Below is only the static mounting and /health.
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class Prompt(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "Go to /static/index.html for the chat UI."}

@app.get("/health")
def health():
    return {"status": "ok"}

# Keep your /generate endpoint from Module 6.
```

Run:
```bash
uvicorn app:app --reload --port 8000
```

Visit:
```
http://localhost:8000/static/index.html
```

#### Expected Result
You see the chat page; sending a prompt returns a model response.

#### Common Issues & Fixes
- **404 for index.html** → Ensure the file is at `static/index.html`.  
- **CORS errors** → Make sure you’re accessing the page via the same origin (`/static` on your FastAPI server).  
- **No /generate** → Ensure Module 6 endpoint exists and returns `{ "response": "..." }`.

#### Mini Success Moment
> ✔️ UI + API are talking locally.

---

### Step 3 — UX Polish (Optional)
**Goal:** Make chatting smoother.  
**Ideas:**
- Disable the send button while a request is pending (already done).  
- Keep focus on the input after sending (done).  
- Auto‑scroll the log (done).  
- Show multi‑line prompts with Shift+Enter (done).

---

## 4. Checkpoint Test
- You can open `http://localhost:8000/static/index.html`.  
- Typing a message returns an AI response.  
- The log scrolls and the button disables during requests.

> ✔️ If true, Module 7 is complete.

## 5. Troubleshooting Guide
- **“Cannot POST /generate”** → Your backend doesn’t have the endpoint; revisit Module 6.  
- **CORS error** → Always load the page from the same server and port hosting `/generate`.  
- **404 static** → Double‑check the `static` folder path and the `app.mount` line.

## 6. Recap — What You Accomplished
- Built a simple browser chat page  
- Served it with FastAPI on the same origin  
- Successfully chatted with your local model via `/generate`

## 7. What’s Next
In **Module 8**, you’ll make your **local site public** using **Cloudflare Tunnels** and (optionally) point a **custom domain** at it.
