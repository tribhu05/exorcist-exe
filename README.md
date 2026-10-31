# EXORCIST.EXE // Case #1031: The Murder of PID 1
### An Air-Gapped Cyber-Noir OS Murder Mystery & Digital Forensic Interrogation Game
> **Hacktoberfest 2026 Week 4 Official Submission: "Ghost in the Machine"**  
> *Theme: Open-Source AI, Local & Offline Innovation, Zero-Telemetry Data Privacy.*

[![Live Web Demo](https://img.shields.io/badge/PLAY_LIVE-GITHUB_PAGES-00ff66?style=for-the-badge&logo=github&logoColor=black)](https://tribhu05.github.io/exorcist-exe/)
[![CI](https://github.com/tribhu05/exorcist-exe/actions/workflows/ci.yml/badge.svg)](https://github.com/tribhu05/exorcist-exe/actions/workflows/ci.yml)
[![Deploy to GitHub Pages](https://github.com/tribhu05/exorcist-exe/actions/workflows/deploy.yml/badge.svg)](https://github.com/tribhu05/exorcist-exe/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/tribhu05/exorcist-exe)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/tribhu05/exorcist-exe)

```
  ______   _____   _____   _____ _____ _____ _______   ________   ________ 
 |  ____| \ \ / / / ____| / ____|_   _/ ____|__   __| |  ____\ \ / /  ____|
 | |__   __\ V / | |     | (___   | || (___    | |    | |__   \ V /| |__   
 |  __| |___> <  | |      \___ \  | | \___ \   | |    |  __|   > < |  __|  
 | |____   / . \ | |____  ____) |_| |_|___) |  | | _  | |____ / . \| |____ 
 |______| /_/ \_\ \_____|_____/|_____|_____/   |_|(_) |______/_/ \_\______|
  >> CYBER-NOIR OS FORENSICS << CASE #1031: THE MURDER OF PID 1
```

---

## 🎮 Play Instantly Online
You can play the full forensic investigation right now in your browser without installing anything:
👉 **[Launch Forensic Console (Live Demo)](https://tribhu05.github.io/exorcist-exe/)**

Featuring complete CRT phosphor scanlines, procedural audio synthesis, four suspect interrogations, evidence confrontation, and the final Exorcism Indictment trial.

---

## 🔎 The Case Dossier
* **Victim:** `init` (Process ID: 1, Parent of All Processes)
* **Time of Death:** `03:42:19 UTC`
* **Crime Scene:** `Ring 0 / Kernel Address Space 0x7FFF00000000`
* **Watchdog Countdown:** 15 minutes before unrecoverable Kernel Panic

At 03:42:19 UTC, the central heartbeat of the operating system flatlined. PID 1 died from a violent `SIGSEGV` General Protection Fault. You play as **Detective Ray Trace**, an air-gapped Digital Coroner summoned to investigate the crash.

Four primary system daemons have been detained in the interrogation room. One of them is harboring the **Ghost in the Machine**. Examine raw memory hex dumps, cross-examine suspects with contradictory system logs, catch them in lies, and execute the terminal exorcism command before the hardware watchdog timer destroys the mainframe.

---

## ✨ Features & Architecture

### 1. Multi-Persona Open-Weight AI
Interrogate 4 system daemons powered by local open-weight AI (Ollama with Gemma 2 / Llama 3.2, with a high-fidelity built-in offline dialogue matrix):
* **`systemd` (The Chief Administrator):** Arrogant, pedantic, defensive. Claims every unit was compliant.
* **`GarbageCollector` (The Heap Janitor):** Cynical, exhausted, chain-smoker persona. Sees all dangling pointers and dirty leaks.
* **`CronDaemon` (The Clock Watcher):** Twitchy, obsessive-compulsive, has an airtight timestamp alibi.
* **`Daemon 666 (The Phantom Socket)`:** The unregistered ghost process living in unmapped memory. Speaks in riddles and glitched hex.

### 2. Forensic Evidence Locker
Inspect authentic digital artifacts:
* 📄 **Corrupted Syslog (`/var/log/syslog`):** Chronological log of rogue socket binding at 03:42:15 and PID 1 death at 03:42:19.
* 💾 **Stack Memory Hex Dump (`core.dump`):** Real hex & ASCII view showing stack smashing with `0x41` and hijacked Instruction Pointer `RIP = 0x7FFFDEADBEEF`.
* 🌐 **Network Socket Table (`netstat -tulnp`):** Unauthorized raw socket listener on port 666 with hidden PID.
* 🧬 **Cgroup Memory Slices (`/sys/fs/cgroup`):** Rogue cgroup `ghost.slice` escaping sandbox with direct DMA flags.

### 3. Dual Interface: Modern Web HUD + Retro Terminal CLI
* **Web Console (Next.js):** Phosphor green / cyber amber CRT aesthetic, scanline overlays, dynamic glitch animations on high tension, and procedural sound synthesizer (Web Audio API).
* **Terminal CLI (`python cli/detective.py`):** Play the entire case directly inside your terminal with ANSI colors, typing soundscapes, and interactive prompt loops.

### 4. 100% Air-Gapped & Zero Telemetry
* Zero external API keys needed.
* Zero prompts or code sent to corporate cloud servers.
* Runs entirely on your local machine, preserving complete privacy.

---

## 🚀 Quickstart

### Prerequisites
* Python 3.10+
* Node.js 18+ (for Web interface)
* *(Optional)* [Ollama](https://ollama.com/) running locally with `ollama pull gemma2:2b` or `llama3.2:3b`. If Ollama is not installed, the built-in offline expert engine runs automatically.

### Option A: One-Click Startup (Windows PowerShell)
```powershell
./run.ps1
```
* Backend runs on `http://localhost:8000`
* Frontend runs on `http://localhost:3000`

### Option B: Play Directly in Terminal (CLI Mode)
```bash
# Setup backend
cd backend
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate
pip install -r requirements.txt

# Launch CLI Game
python cli/detective.py
```

### Option C: Docker Compose
```bash
docker-compose up --build
```

---

## 🧪 Running the Test Suite
The backend includes 16 automated tests covering API routes, suspect dialogue logic, evidence presentation, and indictment outcomes:
```bash
cd backend
pytest
```

---

## 🏆 Hacktoberfest 2026: Why Open Innovation Matters
Proprietary cloud LLMs demand constant internet access and siphon confidential codebases, system logs, and user telemetry to centralized corporate servers.

**EXORCIST.EXE** proves that open-weight AI (Gemma 2, Llama 3.2, Ollama) can run entirely **on-device, offline, and air-gapped**. It delivers an engaging, responsive multi-agent roleplay and forensic reasoning experience without leaking a single byte over the wire.

Open-source AI belongs to developers.

---

## 📜 License
MIT License — Copyright (c) 2026 Tribhuwan (tribhu05).
