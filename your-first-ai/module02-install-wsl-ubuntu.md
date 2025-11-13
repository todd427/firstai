# Module 2 — Install WSL on Windows (or Ubuntu Linux)
*Set up a developer-friendly Linux environment the easy way. This module includes a Windows WSL path and a native Ubuntu alternative.*

## 1. Before You Begin
### Purpose
You’ll install a Linux environment so you can run developer tools reliably. On Windows, we’ll use **WSL (Windows Subsystem for Linux)**. If you prefer, there’s an **Alternative Path** to install **Ubuntu** natively.

### What You’ll Need
- A Windows 10/11 PC **or** a computer for native Ubuntu install
- Internet access
- Admin permission (for WSL)
- 45–90 minutes
- Difficulty: ★★☆ (still beginner-friendly)

### Why This Matters
Most AI tooling assumes Linux. WSL gives you Linux on Windows without dual-booting, and Ubuntu gives you the full Linux experience. Either way, this unlocks everything that follows.

## 2. Overview of Steps
1. Enable and install WSL (Windows path).  
2. Verify WSL version and install Ubuntu from Store.  
3. Do a quick Linux success test.  
4. **Alternative Path:** Create a bootable USB and install Ubuntu natively.

---

## 3. Step-by-Step Instructions (Windows + WSL)

### Step 1 — Enable and Install WSL
**Goal:** Turn on WSL and install the Linux subsystem.  
**Why:** This prepares Windows to run Linux apps.

#### Instructions (PowerShell as Administrator)
1. Press **Start**, type **PowerShell**.  
2. Right‑click **Windows PowerShell** → **Run as administrator**.  
3. Paste the command below and press **Enter**:
```powershell
wsl --install
```
> If you already have WSL, you may see a message saying it’s installed. That’s OK.

#### Expected Result
Windows installs WSL (and may ask for a restart). If prompted, **restart** your PC.

#### Common Issues & Fixes
- **“wsl is not recognized”** → Your Windows version may be too old. Run `winver`. Update Windows, then try again.
- **Feature missing** → Ensure “Virtual Machine Platform” and “Windows Subsystem for Linux” features are enabled (Windows turns them on automatically with `wsl --install`).

#### Mini Success Moment
> ✔️ WSL is now enabled. You’re about to have Linux on Windows.

---

### Step 2 — Set WSL to Version 2 (Recommended)
**Goal:** Make sure you’re using WSL 2.  
**Why:** WSL 2 is faster and more compatible.

#### Instructions (PowerShell or Command Prompt)
```powershell
wsl --set-default-version 2
wsl --status
```
Look for a line like: `Default Version: 2`

#### Expected Result
You see **Default Version: 2**. If not, run Windows Update, reboot, and try again.

#### Common Issues & Fixes
- **Default is 1** → Run Windows Update, reboot, then set default to 2 again.

#### Mini Success Moment
> ✔️ WSL 2 set. You’re on the recommended version.

---

### Step 3 — Install Ubuntu from the Microsoft Store
**Goal:** Get a Linux distribution to run inside WSL.  
**Why:** Ubuntu is beginner‑friendly and well‑documented.

#### Instructions
1. Open the **Microsoft Store**.  
2. Search for **Ubuntu** (choose “Ubuntu” or “Ubuntu 22.04 LTS”).  
3. Click **Get/Install**.  
4. Launch **Ubuntu** from the Start menu.  
5. When prompted, create a **UNIX username** and **password** (lowercase is standard).

#### Expected Result
You see a Linux terminal prompt like:
```
username@HOSTNAME:~$
```

#### Common Issues & Fixes
- **Stuck on “Installing”** → Close the Store, reboot, try again. Ensure `wsl --status` works.
- **No network in Ubuntu** → In Ubuntu, try `sudo apt update`. If it fails, restart Windows and relaunch Ubuntu.

#### Mini Success Moment
> ✔️ You have a Linux shell on Windows. Nice.

---

### Step 4 — Update Packages (Inside Ubuntu)
**Goal:** Bring Ubuntu up to date.  
**Why:** Avoids weird errors later.

#### Instructions (in Ubuntu)
```bash
sudo apt update && sudo apt -y upgrade
sudo apt -y install git curl build-essential python3 python3-venv python3-pip
python3 --version
pip3 --version
```
> Enter your password if prompted.

#### Expected Result
You see version numbers for Python and pip, and no errors on install.

#### Common Issues & Fixes
- **“Could not get lock /var/lib/dpkg/lock”** → Wait a minute; another process is finishing. Try again.
- **Broken packages** → Run `sudo apt --fix-broken install` and re-run the update.

#### Mini Success Moment
> ✔️ Your Linux environment is ready for development.

---

### Step 5 — Your First Linux Command (Confidence Win)
**Goal:** Try a harmless command.  
**Why:** Reinforces success.

#### Instructions
```bash
echo "Hello from Your First AI on WSL"
```

#### Expected Result
It prints exactly: `Hello from Your First AI on WSL`

#### Mini Success Moment
> ✔️ You ran your first Linux command inside WSL.

---

## Alternative Path — Install Ubuntu Natively (No WSL)
*Do this only if you intend to run Linux full‑time on the machine.*

### Step A — Create a Bootable USB
**Goal:** Make an installer you can boot from.  
**Why:** This is how you start a clean Ubuntu install.

#### Instructions
1. Download the latest **Ubuntu Desktop ISO** from ubuntu.com.  
2. Use a USB tool (e.g., **Rufus** on Windows) to write the ISO to a 8+ GB USB stick.  
3. Safely eject the USB.

#### Expected Result
A bootable Ubuntu USB installer.

### Step B — Install Ubuntu
**Goal:** Install Ubuntu as your primary OS (or dual‑boot, if advanced).  
**Why:** Full Linux environment with no Windows layer.

#### Instructions
1. Boot from the USB (change boot order in BIOS if needed).  
2. Choose **Install Ubuntu**.  
3. Follow on‑screen steps. Use **Install alongside** only if you understand dual‑boot.  
4. Create a username and password.  
5. After install, reboot and remove USB.

#### Step C — First Setup
```bash
sudo apt update && sudo apt -y upgrade
sudo apt -y install git curl build-essential python3 python3-venv python3-pip
python3 --version
pip3 --version
```
> ✔️ Same expected results as WSL path.

---

## 4. Checkpoint Test
- **Windows path:**  
  - `wsl --status` shows **Default Version: 2**  
  - Ubuntu launches and `python3 --version` prints a version  
- **Ubuntu native path:**  
  - System boots into Ubuntu  
  - `python3 --version` prints a version

> ✔️ If these are true, you’ve completed Module 2.

## 5. Troubleshooting Guide
- **WSL still on version 1** → Update Windows fully, reboot, `wsl --set-default-version 2` again.  
- **Ubuntu won’t install from Store** → `wsl --install`, reboot, try Store again.  
- **No internet in Ubuntu** → Reboot; verify Windows networking; try `sudo apt update`.  
- **Permission denied** → Use `sudo` when installing packages.

## 6. Recap — What You Accomplished
- Installed **WSL** (or **Ubuntu** natively)  
- Verified **Python** and **pip** are working  
- Ran your first Linux command successfully

## 7. What’s Next
In **Module 3**, you’ll create accounts for **GitHub** and **HuggingFace**, set up **SSH keys**, and learn how to store **tokens** safely in a `.env` file.
