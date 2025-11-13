# Module 8 — Cloudflare Tunnels + Custom Domain Basics
*Make your local FastAPI app available on the internet safely using Cloudflare Tunnels. Optionally point a custom domain at it.*

## 1. Before You Begin
### Purpose
You’ll expose your local FastAPI server to the internet using **Cloudflare Tunnels**, then (optionally) connect a **custom domain** so others can access your site securely over HTTPS.

### What You’ll Need
- Modules 1–7 completed
- A Cloudflare account (free) — email + password
- Your FastAPI app running locally (e.g., on `http://localhost:8000`)
- (Optional) A domain you control (via Cloudflare, Blacknight, Namecheap, etc.)
- 30–60 minutes
- Difficulty: ★★☆

### Why This Matters
Tunnels let you share your local site without opening router ports or paying for a server. Cloudflare handles HTTPS and global routing for free.

## 2. Overview of Steps
1. Create a free Cloudflare account.  
2. Install `cloudflared`.  
3. Run a quick one‑off tunnel for instant sharing.  
4. Create a **named tunnel** for persistence.  
5. (Optional) Connect a **custom domain** (CNAME).  
6. Verify HTTPS and test externally.  
7. (Optional) Run tunnel on startup (systemd).

---

## 3. Step‑by‑Step Instructions

### Step 1 — Create a Cloudflare Account
**Goal:** Set up your account so Cloudflare can manage tunnels and (optionally) DNS.  
**Why:** Tunnels are tied to your Cloudflare login.

#### Instructions
1. Visit **https://dash.cloudflare.com/sign-up** and create a free account.  
2. Verify your email.  
3. (Optional) If you own a domain elsewhere (e.g., **Blacknight**, **Namecheap**), you can later move DNS to Cloudflare or keep DNS at your registrar and use a CNAME (explained below).

#### Mini Success Moment
> ✔️ You’re in the Cloudflare dashboard.

---

### Step 2 — Install `cloudflared`
**Goal:** Add the tunnel tool on your machine.  
**Why:** This program connects your local port to Cloudflare.

#### Instructions (Ubuntu/WSL)
```bash
# Install cloudflared (official repo method)
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -O cloudflared.deb
sudo dpkg -i cloudflared.deb || sudo apt -y -f install
cloudflared --version
```

> On macOS: `brew install cloudflared`  
> On Windows (outside WSL): download the MSI from Cloudflare’s docs.

#### Expected Result
`cloudflared --version` prints a version number.

#### Mini Success Moment
> ✔️ The tunnel tool is installed.

---

### Step 3 — Quick Share (One‑Off Tunnel)
**Goal:** Get a public URL immediately.  
**Why:** Fastest way to share your local site.

#### Instructions
Keep your FastAPI app running on port **8000**, then in another terminal:
```bash
cloudflared tunnel --url http://localhost:8000
```
Watch the output. Look for a line like:
```
INFO | Your quick tunnel has been created! Visit it at:
https://<random-subdomain>.trycloudflare.com
```

Copy that URL and open it in a browser (or share it with a friend).

#### Expected Result
Your local site is publicly visible with HTTPS.

#### Common Issues & Fixes
- **Backend not reachable** → Ensure FastAPI is running on `localhost:8000`.  
- **Firewall blocks** → Temporarily allow the process or try another port.

#### Mini Success Moment
> ✔️ You just put your local site on the internet.

> Note: Quick tunnels are temporary. For a stable URL, create a **named tunnel**.

---

### Step 4 — Create a Named Tunnel (Persistent)
**Goal:** Set up a tunnel with a stable ID and config file.  
**Why:** Enables consistent URLs, multiple services, and auto‑start.

#### Instructions
1. **Authenticate cloudflared** (opens a browser):
```bash
cloudflared login
```
2. **Create a tunnel** (name it something short):
```bash
cloudflared tunnel create my-tunnel
```
This prints an ID and creates credentials in `~/.cloudflared/`.

3. **Create a config file** at `~/.cloudflared/config.yml`:
```bash
nano ~/.cloudflared/config.yml
```
Paste and adjust as needed:
```yaml
tunnel: my-tunnel
credentials-file: /home/youruser/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: localhost
    service: http://localhost:8000
  - service: http_status:404
```
(You can add multiple services later.)

4. **Run the tunnel with config**:
```bash
cloudflared tunnel run my-tunnel
```

#### Expected Result
Tunnel connects and routes to your local app. You’ll see logs confirming connections.

#### Mini Success Moment
> ✔️ You have a named, persistent tunnel.

---

### Step 5 — (Optional) Connect a Custom Domain
**Goal:** Use a friendly name like `ai.yourdomain.com`.  
**Why:** Easier to remember and share.

#### Option A — Your DNS Is Already on Cloudflare
1. In Cloudflare Dashboard → **Websites** → select your domain.  
2. Go to **DNS** → **Records** → **Add record**.  
3. **Type:** `CNAME`  
   **Name:** `ai` (or whatever subdomain you want)  
   **Target:** The tunnel’s public hostname (Cloudflare will show it, e.g., `uuid.cfargotunnel.com`)  
   **Proxy status:** **Proxied** (orange cloud)  
4. Save.

#### Option B — DNS Elsewhere (e.g., Blacknight)
1. Log in to your registrar (Blacknight, etc.).  
2. Add a **CNAME** record:  
   **Name:** `ai`  
   **Value/Target:** `uuid.cfargotunnel.com` (from Cloudflare)  
3. In Cloudflare, add the same CNAME for visibility or use **Cloudflare for SaaS** (advanced).  
4. Wait for DNS to propagate (can take minutes).

#### Verify
Visit `https://ai.yourdomain.com`. You should see your site.

#### Common Issues & Fixes
- **DNS not found** → Wait for propagation; verify the exact CNAME target.  
- **SSL errors** → Ensure Proxy (orange cloud) is on; Cloudflare handles TLS for you.  
- **Wrong target** → Use the **tunnel’s** hostname, not your local IP.

#### Mini Success Moment
> ✔️ Your site has a real name on the public internet.

---

### Step 6 — Verify HTTPS and External Access
**Goal:** Confirm anyone can reach your site securely.  
**Why:** Avoid false positives that only work locally.

#### Instructions
- Test on your **phone** using mobile data (not Wi‑Fi).  
- Visit the tunnel URL or your custom domain.  
- Load your **/health** route: `https://ai.yourdomain.com/health`

#### Expected Result
You see your health JSON. If the UI is served at `/static/index.html`, load that too.

#### Mini Success Moment
> ✔️ External verification complete.

---

### Step 7 — (Optional) Run Tunnel on Startup (systemd)
**Goal:** Keep the tunnel running after reboots.  
**Why:** Reliability.

#### Instructions (Ubuntu/WSL)
```bash
# Install/enable the Cloudflare service
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl status cloudflared
```
Ensure your `~/.cloudflared/config.yml` references the correct `tunnel:` name and `credentials-file:` path.

#### Mini Success Moment
> ✔️ Your tunnel starts automatically.

---

## 4. Checkpoint Test
- Quick tunnel works (`cloudflared tunnel --url http://localhost:8000`).  
- Named tunnel runs (`cloudflared tunnel run my-tunnel`).  
- (Optional) Custom domain `CNAME` resolves to the tunnel and loads over HTTPS.  
- External device (phone) can reach `/health` and your chat UI.

> ✔️ If all true, Module 8 is complete.

## 5. Troubleshooting Guide
- **Tunnel connects but site 502/404** → Check your local app is running and the `service` URL matches (`http://localhost:8000`).  
- **CNAME points to wrong target** → Confirm the **tunnel** hostname (often ends with `.cfargotunnel.com`).  
- **Port conflicts** → Run your FastAPI app on another port and update `service:`.  
- **WSL + Windows networking** → If accessing from Windows browser, use `http://localhost:8000`; cloudflared runs inside WSL or Windows—be consistent.  
- **Access control** → Cloudflare Access (One‑Time PIN, Google login) can protect your site (advanced).

## 6. Recap — What You Accomplished
- Installed and ran Cloudflare Tunnels  
- Got an instant public URL (quick tunnel)  
- Created a named, persistent tunnel  
- (Optionally) connected a custom domain via CNAME  
- Verified HTTPS and external reachability

## 7. What’s Next
In **Module 9**, you’ll run **final tests** (load, mobile, break‑and‑fix) and prepare a **launch checklist** to share your AI site responsibly.
