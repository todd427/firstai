# Module 4 — Working with Repos (Clone, Fork, Branch, Commit, Push, Integrity Test)
*Learn the core Git and GitHub workflow so you can safely copy a project, make it your own, and verify it works.*

## 1. Before You Begin
### Purpose
You’ll fork a repository on GitHub, clone it to your machine, create and switch to a new branch, make a small edit, commit it, and push it back to your fork. Then you’ll run a simple integrity test to prove everything is connected and working.

### What You’ll Need
- Module 3 completed (GitHub account, SSH keys working)
- A test repository to fork (you can use any public repo; for practice, choose a tiny one)
- 30–60 minutes
- Difficulty: ★★☆

### Why This Matters
Every AI project you touch will live in a repository. Knowing how to fork, clone, branch, and commit is table stakes. After this module, you’ll be able to collaborate and keep your work cleanly separated from the original.

## 2. Overview of Steps
1. Fork a repo on GitHub (make your own copy in the cloud).  
2. Clone your fork to your computer.  
3. Add the original as “upstream” (optional but professional).  
4. Create and switch to a new branch.  
5. Make a small edit (README).  
6. Commit and push your changes.  
7. Run an integrity test to confirm your setup.

---

## 3. Step-by-Step Instructions

### Step 1 — Fork a Repository
**Goal:** Create your own copy of a project on GitHub.  
**Why:** Keeps your work separate while preserving a link to the original.

#### Instructions
1. Visit a small public repo on GitHub.  
2. Click **Fork** (top-right).  
3. Choose your account; leave settings default; click **Create fork**.

#### Expected Result
You now see the repository under **your** username (e.g., `github.com/yourname/repo-name`).

#### Mini Success Moment
> ✔️ You have your own copy in the cloud.

---

### Step 2 — Clone Your Fork (to your machine)
**Goal:** Download your fork to your computer.  
**Why:** You’ll edit and run the project locally.

#### Instructions (in terminal)
Get the SSH URL from your fork (looks like `git@github.com:yourname/repo-name.git`) and run:
```bash
cd ~
git clone git@github.com:YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME
```

#### Expected Result
A new folder named `REPO_NAME` exists and `git status` shows you’re on `main` or `master`.

#### Common Issues & Fixes
- **Permission denied (publickey)** → SSH key not added; repeat Module 3’s SSH steps.
- **Repo not found** → Make sure you cloned **your fork**, not the original.

#### Mini Success Moment
> ✔️ The code is on your machine.

---

### Step 3 — Add the Original as “upstream” (Professional Practice)
**Goal:** Keep a link to the source repo so you can pull future updates.  
**Why:** This is how you stay in sync with the original project.

#### Instructions
Find the original repo’s SSH URL (e.g., `git@github.com:ORIGINAL_OWNER/REPO_NAME.git`) and run:
```bash
git remote add upstream git@github.com:ORIGINAL_OWNER/REPO_NAME.git
git remote -v
```
You should see two remotes: `origin` (your fork) and `upstream` (original).

#### Mini Success Moment
> ✔️ You’re linked like a pro.

---

### Step 4 — Create and Switch to a New Branch
**Goal:** Do your work on a branch, not on `main`.  
**Why:** Keeps history clean and makes merging easy.

#### Instructions
```bash
git checkout -b feature/readme-tweak
git branch
```
You should see `* feature/readme-tweak` indicating you’re on the new branch.

#### Mini Success Moment
> ✔️ You’re working the way teams do.

---

### Step 5 — Make a Small Edit
**Goal:** Confirm your edit/push pipeline works.  
**Why:** A tiny change proves end-to-end success.

#### Instructions
Open the README in a text editor and add a line at the bottom, for example:
```
Learning Git with Your First AI — it works!
```
Then save the file.

#### Expected Result
`git status` shows the README changed.

#### Mini Success Moment
> ✔️ You changed the project safely.

---

### Step 6 — Commit and Push
**Goal:** Save your work and send it to your fork.  
**Why:** This is how your changes show up on GitHub.

#### Instructions
```bash
git add README.md
git commit -m "docs: add proof-of-life line in README"
git push -u origin feature/readme-tweak
```
Visit your fork on GitHub — you should see your new branch and commit.

#### Mini Success Moment
> ✔️ Your change is live on GitHub.

---

### Step 7 — Integrity Test (Scripted)
**Goal:** Confirm your repo is yours, branched, and connected.  
**Why:** Sanity check before real projects.

#### Instructions
Run this one-liner in your repo:
```bash
python3 - << 'PY'
import os, subprocess, json
def run(cmd):
    return subprocess.check_output(cmd, shell=True).decode().strip()
remote = run("git remote -v")
branch = run("git rev-parse --abbrev-ref HEAD")
origin = run("git remote get-url origin")
status = run("git status --porcelain")
print(json.dumps({
    "branch": branch,
    "origin": origin,
    "remotes": remote.splitlines(),
    "uncommitted_changes": bool(status)
}, indent=2))
PY
```
**Expected Output:**  
- `branch` should be your feature branch (not `main`)  
- `origin` should point to **your** GitHub fork  
- `remotes` includes `upstream` (optional but recommended)  
- `uncommitted_changes` is `false` (you pushed your work)

#### Mini Success Moment
> ✔️ Your repo passes the integrity test.

---

## 4. Checkpoint Test
- Fork exists under your account.  
- Local clone points `origin` to your fork.  
- You’re on a feature branch.  
- A change was committed and pushed.  
- The integrity script shows expected values.

> ✔️ If all true, you’ve completed Module 4.

## 5. Troubleshooting Guide
- **Cloned the original by mistake** → Re-clone using your fork’s SSH URL.  
- **Permission denied** → Ensure SSH keys are loaded (`ssh-add -l`), or use HTTPS + PAT.  
- **Pushed to main by accident** → Create a branch, reset main locally, and force-pull from your fork’s main.  
- **Integrity script errors** → Ensure you’re in the repo directory.

## 6. Recap — What You Accomplished
- Forked a repo and cloned your fork  
- Added `upstream` (professional sync)  
- Created a feature branch  
- Committed and pushed changes  
- Verified with a scripted integrity test

## 7. What’s Next
In **Module 5**, you’ll verify your repo **runs locally without an LLM** — testing imports, routes, file structure, and fixing common errors before you add any AI model.
