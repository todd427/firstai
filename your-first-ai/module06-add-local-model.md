# Module 6 — Add a Small Local Model and Do Your First Generation
*Two beginner‑friendly paths: (A) llama‑cpp (fastest on CPUs) or (B) Transformers (standard Python stack). You’ll run your first real AI completion locally.*

## 1. Before You Begin
### Purpose
You’ll add a small local language model to your working environment and generate your first response. To keep things smooth on most machines, we’ll use a tiny model.

### What You’ll Need
- Modules 1–5 completed
- 1–2 GB free disk space
- Internet access
- Difficulty: ★★☆

### Why This Matters
Once you’ve proven the “pipes” (Module 5), adding a local model shows you can run AI without cloud costs. It’s your first real end‑to‑end AI result.

## 2. Overview of Steps
1. Choose your path (A: llama‑cpp, B: Transformers).  
2. Install the library.  
3. Download a tiny chat model.  
4. Run a short generation test.  
5. (Optional) Hook it into your FastAPI app.

---

## 3. Path A — **llama‑cpp‑python** (recommended for most CPUs)
*Runs quantized **GGUF** models efficiently on CPUs (and can use GPUs if present). Lightweight and simple.*

### Step A1 — Install llama‑cpp‑python
**Goal:** Add the runtime for GGUF models.  
**Why:** It’s optimized for small machines.

#### Instructions (inside your project venv)
```bash
source .venv/bin/activate
pip install --upgrade pip
pip install llama-cpp-python
```

#### Expected Result
`pip` installs without errors.

---

### Step A2 — Download a Tiny Chat Model (GGUF)
**Goal:** Get a small, CPU‑friendly model.  
**Why:** Faster downloads, quicker tests.

We’ll use **TinyLlama‑1.1B‑Chat** in a 4‑bit quantized file.

#### Instructions
```bash
mkdir -p models && cd models
# Download a 4-bit quantized TinyLlama chat model (about ~0.3–0.5 GB)
wget -O tinyllama-chat.Q4_K_M.gguf   https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
cd ..
```

> If `wget` is missing: `sudo apt -y install wget`

---

### Step A3 — First Generation (Python one‑liner)
**Goal:** See the model reply to a prompt.  
**Why:** Confidence and proof it works.

#### Instructions
```bash
python3 - << 'PY'
from llama_cpp import Llama
llm = Llama(model_path="models/tinyllama-chat.Q4_K_M.gguf", n_ctx=2048)
out = llm(prompt="You are a helpful tutor. In one sentence, say hello to a new learner.", max_tokens=64)
print(out["choices"][0]["text"].strip())
PY
```

#### Expected Result
A short greeting sentence printed to the terminal.

#### Common Issues & Fixes
- **File not found** → Check the filename in `models/`.  
- **Slow on first run** → The first load can take 10–30 seconds on CPUs; that’s normal.

#### Mini Success Moment
> ✔️ You ran a local AI model on your own machine.

---

### Step A4 — Optional: Add an Endpoint to Your FastAPI App
**Goal:** Call the model from your web server.  
**Why:** Turns your model into a service.

Create or edit `app.py` (from Module 5) and add:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

app = FastAPI()

llm = Llama(model_path="models/tinyllama-chat.Q4_K_M.gguf", n_ctx=2048)

class Prompt(BaseModel):
    prompt: str

@app.get("/health")
def health():
    return {"status": "ok", "message": "Your First AI — non‑LLM stack works."}

@app.post("/generate")
def generate(p: Prompt):
    out = llm(prompt=p.prompt, max_tokens=128, temperature=0.7)
    text = out["choices"][0]["text"]
    return {"response": text}
```

Run it:
```bash
uvicorn app:app --reload --port 8000
```

Test it in another terminal:
```bash
curl -s -X POST http://localhost:8000/generate   -H "Content-Type: application/json"   -d '{"prompt":"Give me one fun fact about penguins."}'
```

**Expected:** A short JSON with a “response” field.

---

## 4. Path B — **Transformers** (standard Python stack)
*Heavier install, but the most common ecosystem.*

### Step B1 — Install Transformers + Accelerate
```bash
source .venv/bin/activate
pip install --upgrade pip
pip install "transformers>=4.44" accelerate torch --extra-index-url https://download.pytorch.org/whl/cpu
```
> If you have a compatible NVIDIA GPU and drivers, install torch with CUDA instead of the CPU wheel.

---

### Step B2 — Pick a Tiny Chat Model
**Recommended:** `TinyLlama/TinyLlama-1.1B-Chat-v1.0` (CPU‑friendly).

### Step B3 — First Generation (Transformers)
Create `gen.py`:
```python
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, device_map="auto")
pipe = pipeline("text-generation", model=model, tokenizer=tok)

out = pipe("You are a helpful tutor. In one sentence, greet a new learner.", max_new_tokens=50, do_sample=True)
print(out[0]["generated_text"])
```

Run:
```bash
python3 gen.py
```

**Expected:** A short greeting line printed to the terminal.

---

### Optional: FastAPI Endpoint (Transformers)
```python
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

app = FastAPI()

MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, device_map="auto")
pipe = pipeline("text-generation", model=model, tokenizer=tok)

class Prompt(BaseModel):
    prompt: str

@app.get("/health")
def health():
    return {"status": "ok", "message": "Your First AI — Transformers path."}

@app.post("/generate")
def generate(p: Prompt):
    out = pipe(p.prompt, max_new_tokens=128, do_sample=True)
    return {"response": out[0]["generated_text"]}
```

Run:
```bash
uvicorn app:app --reload --port 8000
```

Test:
```bash
curl -s -X POST http://localhost:8000/generate   -H "Content-Type: application/json"   -d '{"prompt":"Give me a single fun fact about penguins."}'
```

---

## 5. Checkpoint Test
- Path A (llama‑cpp): A local generation prints in terminal and `/generate` returns JSON.  
- Path B (Transformers): `python3 gen.py` prints a completion and `/generate` returns JSON.

> ✔️ If either path works, you’ve completed Module 6.

## 6. Troubleshooting Guide
- **Very slow on CPU:** Start with llama‑cpp and a tiny GGUF; avoid huge models for now.  
- **Out of memory:** Use smaller models or lower precision (e.g., Q4_K_M GGUF). Close heavy apps.  
- **Torch install issues:** Use the CPU wheel shown above first; upgrade later to GPU with correct CUDA.  
- **Model not found / permission denied:** Some models require accepting a license on HuggingFace; check the model page.

## 7. Recap — What You Accomplished
- Installed a local model runtime (llama‑cpp or Transformers)  
- Downloaded a tiny chat model  
- Generated your first local completion  
- (Optional) Exposed it via FastAPI for a simple API

## 8. What’s Next
In **Module 7**, you’ll **build a simple local web UI** that talks to your `/generate` endpoint, so you can chat in a browser on your machine.
