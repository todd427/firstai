# Module 3 — GitHub, HuggingFace, SSH Keys, Tokens, and `.env`
*Set up your developer identity, create secure keys, and store secrets safely.*

## 1. Before You Begin
### Purpose
You’ll create accounts on **GitHub** and **HuggingFace**, generate **SSH keys** for secure connections, create **access tokens**, and store them safely in a local **`.env`** file. You’ll verify everything with simple tests.

### What You’ll Need
- A working Windows+WSL or Ubuntu environment (from Module 2)
- An email address you can verify
- 30–60 minutes
- Difficulty: ★★☆

### Why This Matters
Modern development requires identity (who you are), access (what you can use), and safety (how you store secrets). This module gives you all three.

## 2. Overview of Steps
1. Create a GitHub account and set up your profile.  
2. Generate an SSH key pair and connect it to GitHub.  
3. Create a GitHub Personal Access Token (PAT) for HTTPS operations if needed.  
4. Create a HuggingFace account and access token.  
5. Create a `.env` file to store secrets safely.  
6. Verify everything with connection tests.

---

## 3. Step-by-Step Instructions

### Step 1 — Create Your GitHub Account
**Goal:** Get a GitHub account for storing and collaborating on code.  
**Why:** Almost every open‑source project and tutorial assumes GitHub.

#### Instructions
1. Go to **https://github.com** and click **Sign up**.  
2. Use a strong password (use a password manager).  
3. Verify your email address.  
4. (Optional) Set a public name and short bio on your profile.

#### Expected Result
You can sign in to github.com and see your profile page.

#### Mini Success Moment
> ✔️ You’re on GitHub. You’re now part of the open‑source world.

---

### Step 2 — Generate an SSH Key Pair (on Linux/WSL)
**Goal:** Create a secure key pair for Git operations without typing passwords.  
**Why:** SSH is the standard for secure Git connections.

#### Instructions (in Ubuntu/WSL terminal)
```bash
# Replace with your actual email
ssh-keygen -t ed25519 -C "you@example.com"
```
Press **Enter** to accept the default file location (`/home/<you>/.ssh/id_ed25519`).  
When asked for a passphrase, you can press **Enter** for none (easier) or set one (more secure).

Add your key to the SSH agent:
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Show your **public** key (copy everything from `ssh-ed25519` to the end of the line):
```bash
cat ~/.ssh/id_ed25519.pub
```

#### Expected Result
You see a long line starting with `ssh-ed25519` — this is your **public** key.

#### Common Issues & Fixes
- **“No such file or directory”** → You typed the path wrong. Use `~/.ssh/id_ed25519.pub`.
- **Agent problems** → Run `eval "$(ssh-agent -s)"` again and then `ssh-add`.

#### Mini Success Moment
> ✔️ You just created cryptographic keys like a pro.

---

### Step 3 — Add Your SSH Key to GitHub
**Goal:** Link your local machine to your GitHub account.  
**Why:** Lets you `git push`/`git pull` over SSH without typing passwords.

#### Instructions
1. In your browser, go to **GitHub → Settings → SSH and GPG keys**.  
2. Click **New SSH key**.  
3. Paste the **public** key you copied (`id_ed25519.pub`).  
4. Name it something like **“Laptop WSL”** and click **Add SSH key**.

#### Expected Result
GitHub shows your key in the SSH keys list.

#### Verify the connection (in terminal):
```bash
ssh -T git@github.com
```
You should see something like:
```
Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.
```

#### Common Issues & Fixes
- **Permission denied (publickey)** → The key isn’t added or the agent isn’t running. Re‑run the `ssh-agent` and `ssh-add` steps and retry.

#### Mini Success Moment
> ✔️ Your machine and GitHub can talk securely.

---

### Step 4 — (Optional) Create a GitHub Personal Access Token (PAT)
**Goal:** Use HTTPS with Git when SSH isn’t convenient.  
**Why:** Some networks block SSH, and some tools prefer HTTPS + PAT.

#### Instructions
1. GitHub → **Settings → Developer Settings → Personal access tokens → Tokens (classic)** or **Fine‑grained tokens**.  
2. Create a token with scopes for **repo** (and **read:org** if needed).  
3. Copy the token once (GitHub won’t show it again).

#### Store the PAT safely — **do not** paste it into code.

#### Mini Success Moment
> ✔️ You have a backup method for Git operations.

---

### Step 5 — Create a HuggingFace Account + Access Token
**Goal:** Access models and datasets on HuggingFace.  
**Why:** Many local models and tools use HuggingFace APIs.

#### Instructions
1. Go to **https://huggingface.co** and click **Sign Up**.  
2. Verify your email.  
3. Go to **Settings → Access Tokens** → **New token** (choose **Read** scope).  
4. Copy the token (this is your **HF_TOKEN**).  
5. (Optional) Accept license terms for specific models on their model pages.

#### Quick CLI test (in terminal):
```bash
pip3 install -q huggingface_hub
python3 - << 'PY'
from huggingface_hub import whoami
print(whoami())
PY
```
If it asks for a token, paste your **HF_TOKEN** for this test only (we’ll store it safely next).

#### Mini Success Moment
> ✔️ Your HuggingFace account works.

---

### Step 6 — Create a `.env` File for Secrets
**Goal:** Store secrets locally without committing them to Git.  
**Why:** Keeps tokens safe and out of your repository.

#### Instructions (in your home directory or project root)
```bash
nano .env
```
Paste the following (replace the example values):
```
# Never commit this file
GITHUB_PAT=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Press **Ctrl+O** (write out), **Enter**, then **Ctrl+X** (exit).

Create a `.gitignore` entry to prevent committing `.env`:
```bash
echo ".env" >> .gitignore
```

(If you don’t have a `.gitignore` yet, this creates one.)

#### Expected Result
You have a `.env` file with tokens and it will not be committed to Git.

#### Mini Success Moment
> ✔️ Your secrets are safe and you look like a professional.

---

### Step 7 — Load `.env` in Python (Preview)
**Goal:** Show how projects read secrets without hard‑coding.  
**Why:** This is standard practice in real apps.

#### Instructions
```bash
pip3 install -q python-dotenv
python3 - << 'PY'
import os
from dotenv import load_dotenv
load_dotenv()
print("HF_TOKEN starts with:", os.getenv("HF_TOKEN", "")[:5])
print("GITHUB_PAT starts with:", os.getenv("GITHUB_PAT", "")[:5])
PY
```
You should see masked starts of your variables.

#### Mini Success Moment
> ✔️ Your app can read secrets securely.

---

## 4. Checkpoint Test
- `ssh -T git@github.com` works without error.  
- You have a **GitHub PAT** (optional backup).  
- You created a **HuggingFace token**.  
- You created a **.env** and added it to **.gitignore**.  
- A Python script can read your environment variables.

> ✔️ If all pass, Module 3 is complete.

## 5. Troubleshooting Guide
- **SSH permission denied** → Re‑add the key to your account; ensure the agent is running; confirm the file paths.  
- **Token leaked into Git** → Immediately revoke the token in your account settings and create a new one.  
- **`.env` not loading** → Ensure `python-dotenv` is installed and `load_dotenv()` is called before reading.  
- **HuggingFace model access denied** → Accept the model license on the model page, or check token scopes.

## 6. Recap — What You Accomplished
- GitHub account created and linked via SSH  
- (Optional) GitHub PAT created for HTTPS  
- HuggingFace account + token working  
- Secrets stored safely in a `.env` file  
- Python can access your secrets securely

## 7. What’s Next
In **Module 4**, you’ll **work with repositories**: clone, fork, create branches, make your first commit, and verify everything with a simple integrity test.
