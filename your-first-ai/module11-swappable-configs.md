# Module 11 — Swappable Model Configs (YAML + Env Flags)
*Switch models and backends (llama‑cpp vs Transformers) without editing app code. You’ll add a `config.yaml`, read env flags, and boot the right runtime at startup.*

## 1. Before You Begin
### Purpose
You’ll separate **configuration** from **code**, so you can swap models, quant files, and even runtimes (llama‑cpp vs Transformers) without rewriting your app. This is how real projects stay flexible.

### What You’ll Need
- Modules 1–10 completed
- A working FastAPI app from Module 6/7
- 20–40 minutes
- Difficulty: ★★☆

### Why This Matters
Hard‑coding models leads to brittle projects. A simple config file + env flags lets you compare models quickly and avoid mistakes.

---

## 2. Directory Prep
In your project folder, create a `config/` directory:
```bash
mkdir -p config
```

Create `config/config.yaml` and paste this template:
```yaml
# Which backend to use: llama_cpp | transformers
backend: llama_cpp

# Common generation params
generation:
  max_new_tokens: 128
  temperature: 0.7
  top_p: 0.95

# llama-cpp options (GGUF models)
llama_cpp:
  model_path: "models/tinyllama-chat.Q4_K_M.gguf"
  n_ctx: 2048
  n_threads: 0         # 0 = auto
  n_gpu_layers: 0      # >0 to offload layers to GPU (if supported)

# transformers options (HF Hub)
transformers:
  model_id: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
  device_map: "auto"   # "auto" | "cpu" | "cuda"
  torch_dtype: "auto"  # "auto" | "float16" | "bfloat16" | "float32"
```

> You can create multiple YAML files for different presets, e.g., `config/dev.yaml`, `config/fast.yaml`.

---

## 3. Add Environment Flags
Create a `.env` entry (from Module 3) to pick a config at runtime:
```
MODEL_CONFIG=config/config.yaml
BACKEND_OVERRIDE=
```

Rules:
- If `BACKEND_OVERRIDE` is set (e.g., `transformers`), it wins.  
- Otherwise the YAML `backend:` key decides.  
- `MODEL_CONFIG` points to the YAML to load.

Add `.env` to `.gitignore` if not already done.

---

## 4. Loader Utility (`model_loader.py`)
Create a file `model_loader.py` with this content:
```python
import os, yaml
from typing import Any, Dict

def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_config() -> Dict[str, Any]:
    path = os.getenv("MODEL_CONFIG", "config/config.yaml")
    cfg = load_yaml(path)
    override = os.getenv("BACKEND_OVERRIDE", "").strip()
    if override:
        cfg["backend"] = override
    return cfg

# Factories for backends
def make_llama_cpp(cfg: Dict[str, Any]):
    from llama_cpp import Llama
    opt = cfg.get("llama_cpp", {})
    gen = cfg.get("generation", {})
    llm = Llama(
        model_path=opt.get("model_path"),
        n_ctx=opt.get("n_ctx", 2048),
        n_threads=opt.get("n_threads", 0),
        n_gpu_layers=opt.get("n_gpu_layers", 0),
    )
    def generate(prompt: str) -> str:
        out = llm(prompt=prompt,
                  max_tokens=gen.get("max_new_tokens", 128),
                  temperature=gen.get("temperature", 0.7),
                  top_p=gen.get("top_p", 0.95))
        return out["choices"][0]["text"]
    return generate

def make_transformers(cfg: Dict[str, Any]):
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    opt = cfg.get("transformers", {})
    gen = cfg.get("generation", {})
    tok = AutoTokenizer.from_pretrained(opt.get("model_id"))
    model = AutoModelForCausalLM.from_pretrained(
        opt.get("model_id"),
        device_map=opt.get("device_map", "auto"),
        torch_dtype=opt.get("torch_dtype", "auto"),
    )
    pipe = pipeline("text-generation", model=model, tokenizer=tok)
    def generate(prompt: str) -> str:
        out = pipe(prompt,
                   max_new_tokens=gen.get("max_new_tokens", 128),
                   do_sample=True,
                   temperature=gen.get("temperature", 0.7),
                   top_p=gen.get("top_p", 0.95))
        return out[0]["generated_text"]
    return generate

def make_generator():
    cfg = get_config()
    backend = cfg.get("backend", "llama_cpp").lower()
    if backend == "llama_cpp":
        return make_llama_cpp(cfg)
    elif backend == "transformers":
        return make_transformers(cfg)
    else:
        raise ValueError(f"Unknown backend: {backend}")
```

> `make_generator()` returns a function `generate(prompt) -> str` that your app can call, regardless of backend.

---

## 5. Wire It Into FastAPI (`app.py`)
Edit your existing `app.py` to use the loader:
```python
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()  # read MODEL_CONFIG/BACKEND_OVERRIDE

from model_loader import make_generator

app = FastAPI()
generate = make_generator()  # pick backend from config/env

class Prompt(BaseModel):
    prompt: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate")
def generate_route(p: Prompt):
    text = generate(p.prompt)
    return {"response": text}
```

Restart your server:
```bash
uvicorn app:app --reload --port 8000
```

---

## 6. Swap Backends Without Editing Code
**Switch to Transformers temporarily:**
```bash
export BACKEND_OVERRIDE=transformers
uvicorn app:app --reload --port 8000
```

**Use a different YAML:**
```bash
export MODEL_CONFIG=config/fast.yaml
uvicorn app:app --reload --port 8000
```

**Persist across reboots:** Add the exports to your shell profile or `.env` file.

---

## 7. Checkpoint Test
- `POST /generate` works with **llama‑cpp** using your GGUF file.  
- Flip to **Transformers** via `BACKEND_OVERRIDE` and it still works.  
- Point `MODEL_CONFIG` at another YAML and behavior changes accordingly.

> ✔️ If all true, Module 11 is complete.

---

## 8. Troubleshooting
- **Missing YAML library** → `pip install pyyaml`.  
- **FileNotFoundError for model** → Check `model_path` or `model_id`.  
- **Torch/CUDA issues** → Use CPU wheel first; only add CUDA if you know your setup.  
- **Slow loads** → Larger models take time; try a smaller quant or 7B→3B for tests.

---

## 9. What’s Next
In **Module 12**, you’ll add **basic logging and metrics** (latency, tokens, errors) so you can compare models and track performance like a professional.
