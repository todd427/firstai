# Module 1 — Getting Your Gear
*Make sure your computer is ready. Choose to buy or build. Get your first small win.*

## 1. Before You Begin
### Purpose
By the end of this module, you’ll know whether your current computer is good to go, what upgrades (if any) help, and how to choose between buying a ready-made machine or building your own. You’ll also complete a tiny first success test to prove your setup can move forward.

### What You’ll Need
- A Windows or Linux computer (macOS works too, but we’ll focus on Windows + WSL and Ubuntu)
- Internet access
- 30–60 minutes
- Optional: a notepad to track specs and decisions
- Difficulty: ★☆☆ (Beginner)

### Why This Matters
Everything else depends on a stable, confidence-building start. This module prevents “I can’t do this” by giving you clear choices, a readiness test, and a plan.

## 2. Overview of Steps
1. Check your current computer’s key specs (RAM, SSD, CPU).
2. Decide: Buy a computer or (optionally) plan a build.
3. Complete a tiny first success moment.

## 3. Step-by-Step Instructions

### Step 1 — Check Your Specs
**Goal:** Learn if your machine is sufficient.  
**Why:** Most AI tutorials fail because the computer is underpowered or storage is full.

#### Instructions
1. **Windows:** Press `Win + X` → *Task Manager* → *Performance* tab. Note **RAM** and **CPU**.  
   Also open *Settings → System → Storage* and check **Free space**.
2. **Linux:** Open a terminal and run:
```bash
free -h
lscpu | egrep 'Model name|CPU\(s\)|Thread'
df -h ~
```
3. Minimum comfortable baseline to start: **8 GB RAM**, **30+ GB free SSD space**. (16 GB RAM is nicer.)

#### Expected Result
You have a short note: `RAM: __ GB, Free SSD: __ GB, CPU: __`

#### Common Issues & Fixes
- **Low free space:** Uninstall large apps or move files to an external drive / cloud. Aim for 30+ GB free.  
- **Very low RAM (4 GB):** You can still learn, but keep apps closed. Consider upgrading to 8–16 GB later.

#### Mini Success Moment
> ✔️ You now have a realistic picture of your computer. Most people never check—now you did.

---

### Step 2 — Decide: Buy or Build
**Goal:** Choose your path.  
**Why:** Clarity saves money and time.

#### Instructions
**Option A — Buy (recommended for beginners):**
- Look for: 16 GB RAM, 512 GB SSD, recent CPU (Ryzen 5 / Core i5 or newer). A GPU is **not required** to start.
- Consider refurbished to save money.

**Option B — Build (optional adventure):**
- Learn parts: **CPU, Motherboard, RAM, SSD, PSU, Case, (Optional GPU).**
- Use a parts compatibility checker (e.g., PCPartPicker).  
- Plan for: 16 GB RAM, 1 TB SSD if possible.

#### Expected Result
You’ve picked **Buy** or **Build** and have a simple plan (parts list or store short-list).

#### Common Issues & Fixes
- **Overwhelmed by choices:** Stick to the baseline specs and a known brand. Simplicity beats perfection.
- **Worried about building:** You can postpone. Buy now, learn, and build later.

#### Mini Success Moment
> ✔️ You made a decision. That’s momentum.

---

### Step 3 — First Success Moment: Open a Terminal
**Goal:** Do something “developer-y” that anyone can do.  
**Why:** Confidence matters more than clock speed right now.

#### Instructions
- **Windows:** Press `Win`, type `cmd`, and press Enter. Type:
```bash
echo Hello from Your First AI
```
- **Linux:** Open *Terminal* and type the same:
```bash
echo Hello from Your First AI
```

#### Expected Result
You see: `Hello from Your First AI`

#### Common Issues & Fixes
- **Command not found / weird output:** Re-type exactly; copy/paste helps.

#### Mini Success Moment
> ✔️ You ran your first command. You’re on your way.

## 4. Checkpoint Test
- Do you have **8+ GB RAM** and **30+ GB free SSD**?  
- Did you decide **Buy** or **Build**?  
- Did `echo Hello from Your First AI` print correctly?  

> ✔️ If yes to all three, you’re ready for Module 2.

## 5. Troubleshooting Guide
- **I have low resources:** Close apps, clear space, or plan an upgrade. You can still continue to learn.
- **I can’t decide buy vs build:** Choose **Buy** to start; revisit building as an optional project.
- **Terminal is scary:** It’s just text. You already used it successfully.

## 6. Recap — What You Accomplished
- Checked your machine’s readiness  
- Chose a path (buy or build)  
- Had your first success at the terminal

## 7. What’s Next
In **Module 2**, you’ll install **WSL on Windows** (or native **Ubuntu**) and run your first Linux command with confidence.
