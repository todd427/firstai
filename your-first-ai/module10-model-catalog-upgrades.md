# Module 10 — Model Catalog & Choosing Upgrades
*Pick the right model for your machine and your goals. Learn sizes, quantization, RAM/GPU needs, and when to upgrade hardware.*

## 1. Before You Begin
### Purpose
You’ll learn how to choose a model that actually fits your machine, runs at a comfortable speed, and matches your use‑case (chat, coding, teaching, role‑play). You’ll compare **model families**, **parameter sizes**, and **quantization** options, then make a practical choice with an upgrade plan.

### What You’ll Need
- Modules 1–9 completed
- A working local model (from Module 6)
- 20–40 minutes
- Difficulty: ★★☆

### Why This Matters
“Bigger” is not always “better.” The best model is the one that meets your needs **reliably** on **your hardware**. Understanding trade‑offs saves time and money.

---

## 2. Model Families (Plain‑English Overview)
- **General chat models** — good for everyday help, tutoring, summaries.  
- **Instruction‑tuned models** — follow directions well and stay on task.  
- **Coding‑tuned models** — optimized for code completion and debugging.  
- **Long‑context models** — can read longer inputs (docs, transcripts).  
- **Multimodal models** — can handle images or audio (advanced).

> You can start small and swap models later. Your FastAPI interface (Module 6/7) won’t need big changes.

---

## 3. Parameter Sizes & What They Mean
- **1–3B (tiny)** — Runs comfortably on CPUs. Good for basics and demos.  
- **7–9B (small)** — Sweet spot for many laptops/CPUs with quantization; better quality.  
- **13–14B (medium)** — Noticeably stronger; benefits from a GPU or fast CPU.  
- **30–34B (large)** — Strong outputs; GPU helpful or required for speed.  
- **70B+ (extra‑large)** — Usually requires a strong GPU and lots of RAM/VRAM; overkill for beginners.

Rule of thumb (CPU with quantized **GGUF**):  
- **1–3B**: snappy on most CPUs.  
- **7–9B**: usable on modern CPUs; better with small GPU.  
- **13B+**: may feel slow on CPU; shines with GPU acceleration.

---

## 4. Quantization (Why It Helps)
Quantization compresses model weights to use **less memory** and run **faster** with a small quality trade‑off.

Common levels you’ll see (GGUF, for llama‑cpp):  
- **Q2_K** — very small, fastest, lower quality.  
- **Q4_K_M** — balanced for many CPUs (good default).  
- **Q5_K_M** — slightly better quality; needs more RAM.  
- **Q8_0** — near‑full quality; slower; bigger memory footprint.

> Start with **Q4_K_M**. If you have headroom, try **Q5_K_M**. If you need speed, try **Q3_K**/**Q2_K**.

---

## 5. RAM/VRAM Planning (Practical)
- **CPU‑only (no discrete GPU):**  
  - 8 GB RAM: tiny (1–3B) or 4‑bit 7B with patience.  
  - 16 GB RAM: 7B in Q4/Q5 usable; 13B possible but slower.  
  - 32 GB RAM: 13B workable; small long‑context options.  
- **With discrete GPU (6–12 GB VRAM):**  
  - 7B–13B run much faster; use transformer backends with GPU if possible.  
- **Storage:**  
  - Keep **30–60 GB** free to try multiple quant files and libraries.

> Measure, don’t guess. Track generation time per 100 tokens to compare.

---

## 6. Picking by Use‑Case (Decision Tree)
**A. Teaching/Tutoring & General Chat**  
- Start: 3B–7B instruction‑tuned, Q4_K_M.  
- Upgrade: 7B–13B for better reasoning.  
- Long context needs? Pick a long‑context variant.

**B. Coding Help**  
- Start: coding‑tuned 3B–7B.  
- Upgrade: 7B–13B coding‑tuned; switch to GPU if available.

**C. Role‑play / Persona (Players‑style)**  
- Start: 7B instruction‑tuned with warm style.  
- Upgrade: 13B for richer prose and consistency.

**D. Document Q&A / RAG**  
- Start: 7B with embeddings via a separate library.  
- Upgrade: long‑context models or better retrieval pipeline.

**E. On‑device / low‑power**  
- Tiny (1–3B) models quantized to Q4/Q5; accept limits.

---

## 7. Practical Benchmarks You Can Run
Use the same prompt across models and measure speed & quality.

**Speed (tokens/sec)**  
```bash
python3 - << 'PY'
import time, statistics as st
from llama_cpp import Llama
llm = Llama(model_path="models/tinyllama-chat.Q4_K_M.gguf", n_ctx=2048)
times = []
for _ in range(3):
    t0=time.time()
    out = llm(prompt="Summarize the benefits of learning to code in 2 sentences.", max_tokens=128)
    times.append(time.time()-t0)
print("Avg seconds:", round(st.mean(times),2))
PY
```

**Quality (eye test)**  
- Ask: “Explain Python virtual environments to a beginner in 5 sentences.”  
- Check for clarity, correctness, and helpful tone.  
- Compare two models side‑by‑side with the same prompt.

Log results in a simple CSV:
```
model,size,quant,avg_seconds,notes
tinyllama,1.1B,Q4_K_M,3.1,"OK on laptop"
...
```

---

## 8. Upgrade Plan Template
Fill this out after a few tests.

```
Current machine: CPU __, RAM __ GB, (GPU: __ GB VRAM)
Current model: __ (size __B, quant __), speed: __ sec / 128 tok

Goal: (chat / coding / role‑play / long‑context / other)
Pain point: (speed / quality / memory / context length)

Immediate next model to try: __
If not enough, try: __ (size/quant)
If still not enough, hardware plan: (add RAM / add GPU / buy refurbished)

Budget: €__ short‑term, €__ long‑term
```

---

## 9. Common Pitfalls & Fixes
- **Downloaded a massive model by accident** → Use a smaller param size and a quantized file.  
- **RAM/VRAM errors** → Lower quant level or pick a smaller model.  
- **Transformers too slow on CPU** → Try **llama‑cpp** with GGUF.  
- **Great speed but bad answers** → Move from 3B → 7B or 13B.  
- **Context too short** → Use a model with longer context or add retrieval (RAG).

---

## 10. Checkpoint
- You selected 2–3 candidate models that fit your machine.  
- You ran quick speed/quality checks.  
- You wrote an **upgrade plan** with a budget.

> ✔️ If true, Module 10 is complete.

---

## 11. What’s Next
Pick one candidate and move forward. In **Module 11**, you’ll learn how to **swap models cleanly** with a config file and environment flags, so your app can switch between llama‑cpp and Transformers without code edits.
