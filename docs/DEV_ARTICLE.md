---
title: "EXORCIST.EXE: The Ghost in the Machine — An Air-Gapped Cyber-Noir OS Murder Mystery Game"
published: true
tags: devchallenge, hf26challenge, hacktoberfest, opensource
cover_image: https://raw.githubusercontent.com/tribhu05/exorcist-exe/master/docs/banner.png
description: "At 03:42:19 UTC, PID 1 was murdered. An open-weight AI cyber-noir detective game running 100% offline and air-gapped on your laptop."
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 4: Ghost in the Machine](https://dev.to/challenges/hacktoberfest-week4-2026-10-26).*

# EXORCIST.EXE // Case #1031: The Murder of PID 1
### An Air-Gapped Cyber-Noir OS Murder Mystery & Digital Forensic Interrogation Game

> *"Every operating system is a city of invisible workers. But when the parent of all processes dies in unmapped memory, who do you call?"*

---

## 🎮 Demo
* **🌐 Live Web Console (GitHub Pages):** [https://tribhu05.github.io/exorcist-exe/](https://tribhu05.github.io/exorcist-exe/)
* **🚀 1-Click Deploy to Render:** [Deploy on Render](https://render.com/deploy?repo=https://github.com/tribhu05/exorcist-exe)
* **▲ 1-Click Deploy to Vercel:** [Deploy on Vercel](https://vercel.com/new/clone?repository-url=https://github.com/tribhu05/exorcist-exe)

You can launch the forensic investigation directly in your browser without installing anything or providing any API keys!

---

## 💻 Code
* **GitHub Repository:** [https://github.com/tribhu05/exorcist-exe](https://github.com/tribhu05/exorcist-exe)
* **License:** MIT License (100% Open Source)

---

## 🕵️ What I Built
**EXORCIST.EXE** is an interactive, atmospheric **Cyber-Noir Digital Forensics & Murder Mystery Game** powered entirely by **open-weight AI running 100% locally and offline**.

You play as **Detective Ray Trace**, an air-gapped Digital Coroner summoned to Sector `0x7FFF` of a crashed Linux mainframe.

### The Case Briefing
* **Victim:** `init` (PID 1, Parent of All Processes)
* **Time of Death:** `03:42:19 UTC`
* **Crime Scene:** `Ring 0 / Kernel Address Space 0x7FFF00000000`
* **Watchdog Failsafe:** 15 minutes before an unrecoverable hardware Kernel Panic

Four primary system daemons have been detained in the interrogation room. One of them is harboring the **Ghost in the Machine**:
1. **`systemd` (The Arrogant Supervisor):** Pedantic, condescending, defensive. Claims all unit declarations were compliant and refuses to admit oversight.
2. **`GarbageCollector` (The Cynical Heap Janitor):** World-weary, chain-smoking persona. Sweeps memory leaks and knows every dirty reference in the heap.
3. **`CronDaemon` (The Obsessive Clock-Watcher):** Twitchy, paranoid about clock drift down to the nanosecond, with an airtight alibi.
4. **`Daemon 666 (The Phantom Socket)`:** The unregistered ghost process living in unmapped memory. Speaks in riddles, glitching hex, and raw TCP streams.

### Core Gameplay Mechanics
1. **Interactive Open-Weight AI Interrogation:** Converse in real time with each suspect daemon. Suspect personalities, defenses, and tension levels dynamically react to your inquiries.
2. **Authentic Forensic Evidence Locker:** Inspect real system artifacts:
   - Corrupted `/var/log/syslog` timeline showing rogue socket bindings.
   - Stack memory hex dump (`core.dump`) revealing buffer overflow with `0x41414141` and hijacked instruction pointer `RIP = 0x7FFFDEADBEEF`.
   - Network socket tables (`netstat -tulnp`) exposing unauthorized listeners on port 666.
   - Control group records (`/sys/fs/cgroup`) tracking escaped memory slices with direct DMA privileges.
3. **Evidence Confrontation & Dynamic Glitches:** Slam evidence on the table! As suspects get cornered by contradictory logs, their tension gauge surges, glitching their visual text output and triggering distorted audio static.
4. **The Indictment & Terminal Exorcism:** Name the killer process, identify the exploit mechanism, and execute the terminal exorcism command (`kill -9 666` or `sysctl`) to cleanse the operating system!
5. **Dual Interface:** Playable both in a sleek **Next.js Cyber-Noir CRT Web Workstation** and directly inside your console via an authentic **Terminal CLI (`python cli/detective.py`)**!

---

## 🛠️ How I Built It

### Technical Stack & Architecture
- **Open-Weight AI Models:** [Ollama](https://ollama.com/) running **Gemma 2** (`gemma2:2b`) and **Llama 3.2** (`llama3.2:3b`).
- **Resilient Offline Matrix:** Built-in high-fidelity client-side and server-side dialogue matrix ensuring 100% gameplay parity even without Ollama or GPU dependencies.
- **Frontend HUD:** Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS v4, Lucide icons.
- **Backend API:** Python 3.11+, FastAPI, Pydantic v2, SQLite, Pytest (16 automated tests).
- **Procedural Sound FX:** Retro mechanical keyboard typing sounds, terminal hums, glitch bursts, and victory fanfares synthesized purely in real time via the **HTML5 Web Audio API** (zero external audio assets).
- **Automated CI/CD:** GitHub Actions workflows running automated pytest test suites and deploying static exports directly to GitHub Pages.

### Running Locally
```powershell
# One-click start (Windows)
./run.ps1
```
Or play directly inside your terminal:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
pip install -r requirements.txt
python cli/detective.py
```

---

## 🌐 Why Does Open Innovation Matter?
Proprietary cloud AI models lock users behind paywalls and siphon proprietary source code, internal system logs, and user telemetry onto third-party corporate servers.

For digital forensics and security investigations, sending raw memory dumps, stack traces, and network maps to external cloud APIs represents a catastrophic data privacy and compliance hazard.

**EXORCIST.EXE proves the power of open-weight innovation:**
- **Zero Telemetry & 100% Air-Gapped:** Zero corporate API tokens. Not a single byte ever leaves your environment.
- **Offline Autonomy:** Runs anywhere — in a secure vault, in flight, or in offline field scenarios.
- **Community Control:** Open-weight models like Gemma 2 and Llama 3.2 prove that local, compact models possess extraordinary forensic deduction and creative roleplay capabilities when designed with open-source architectures.

Don't let your code become a ghost in the machine. Keep your models open, your inference local, and your sockets monitored! 🎃👻
**EXORCIST.EXE** is an interactive, atmospheric **Cyber-Noir Digital Forensics & Murder Mystery Game** powered entirely by **open-weight AI running 100% locally and offline**.

You play as **Detective Ray Trace**, an air-gapped Digital Coroner summoned to Sector 0x7FFF of a crashed Linux mainframe.

### The Case Briefing
* **Victim:** `init` (PID 1, Parent of All Processes)
* **Time of Death:** `03:42:19 UTC`
* **Crime Scene:** `Ring 0 / Kernel Address Space 0x7FFF00000000`
* **Watchdog Failsafe:** 15 minutes before an unrecoverable hardware Kernel Panic

Four primary system daemons have been detained in the interrogation room. One of them is possessed by the **Ghost in the Machine**:
1. **`systemd` (The Arrogant Bureaucrat):** Pedantic, condescending, defensive. Claims all unit declarations were compliant and refuses to admit oversight.
2. **`GarbageCollector` (The Cynical Heap Janitor):** World-weary, chain-smoking persona. Sweeps memory leaks and knows every dirty reference in the heap.
3. **`CronDaemon` (The Obsessive Clock-Watcher):** Twitchy, paranoid about clock drift down to the nanosecond, with an airtight alibi.
4. **`Daemon 666 (The Phantom Socket)`:** The unregistered ghost process living in unmapped memory. Speaks in riddles, glitching hex, and raw TCP streams.

### Core Gameplay Mechanics
1. **Interactive Open-Weight AI Interrogation:** Converse in real time with each suspect daemon. Their personality traits, defenses, and tension levels adapt to your line of questioning.
2. **Real Forensic Evidence Locker:** Inspect authentic system artifacts:
   - Corrupted `/var/log/syslog` timeline showing rogue socket bindings.
   - Stack memory hex dump (`core.dump`) revealing buffer overflow with `0x41414141` and hijacked instruction pointer `RIP = 0x7FFFDEADBEEF`.
   - Network socket tables (`netstat -tulnp`) exposing unauthorized listeners on port 666.
   - Control group records (`/sys/fs/cgroup`) tracking escaped memory slices.
3. **Confrontation & Glitch Tension:** Slam evidence on the table! As suspects get cornered by contradictory logs, their tension gauge surges, glitching their visual text output and triggering distorted audio static.
4. **The Indictment & Terminal Exorcism:** Name the killer process, identify the exploit mechanism, and execute the terminal exorcism command (`kill -9 666` or `sysctl`) to save the operating system from a fatal Kernel Panic!
5. **Dual Interface:** Playable both in a sleek **Next.js Cyber-Noir CRT Web Workstation** and directly inside your console via an authentic **Terminal CLI (`python cli/detective.py`)**!

---

## 💻 2. Tools & Open-Source AI Stack

- **Open-Weight AI Runtime:** [Ollama](https://ollama.com/) running **Gemma 2** (`gemma2:2b`) and **Llama 3.2** (`llama3.2:3b`).
- **Offline Heuristic Matrix:** High-fidelity zero-dependency offline fallback engine ensuring the game is 100% playable even without Ollama installed or prior weight downloads!
- **Backend:** Python 3, FastAPI, Pydantic v2, SQLite, Pytest (16 automated tests).
- **Frontend:** Next.js 16 (App Router), TypeScript, Tailwind CSS, Lucide icons.
- **Procedural Sound FX:** Retro mechanical keyboard typing sounds, terminal blips, glitch bursts, and victory fanfares synthesized purely in real time via the **HTML5 Web Audio API** (zero audio file downloads required).
- **Aesthetic:** Phosphor green (`#00FF66`), cyber amber (`#FFB000`), scanlines, screen curvature, and custom CRT flicker shaders.

---

## 🔒 3. Why Open Innovation & Local AI Matter
Proprietary cloud AI models lock users into costly monthly subscriptions and siphon proprietary codebases, internal crash dumps, and confidential chat logs onto centralized corporate servers.

For a forensic developer tool or security investigation platform, sending internal stack traces or network topologies to third-party cloud APIs is a catastrophic compliance and security risk.

**EXORCIST.EXE embodies the true spirit of Hacktoberfest Week 4 ("Ghost in the Machine"):**
- **100% Air-Gapped:** Zero telemetry. Zero API tokens. Not a single byte ever leaves your local machine.
- **Offline Resilience:** Runs seamlessly on a laptop in an airplane, in an air-gapped security vault, or in an off-grid environment.
- **Open Weights for Open Minds:** Proves that compact open-weight models (like Gemma 2 2B and Llama 3.2 3B) possess incredible roleplay, reasoning, and forensic deductive capabilities when paired with creative prompt architectures.

---

## 🕹️ 4. How to Play Locally

### Option 1: Web Console (One-Click Launch)
```powershell
./run.ps1
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### Option 2: Terminal CLI Mode
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Run the detective game
python cli/detective.py
```

### Option 3: Docker Compose
```bash
docker-compose up --build
```

---

## 🧪 5. Testing & Code Quality
The repository comes equipped with a comprehensive automated test suite verifying suspect persona consistency, evidence presentation, indictment scoring, and API routes:
```bash
cd backend
pytest
```
*Result: 16 passed in 25.93s with 100% passing tests.*

---

## 💡 6. Reflections on Hacktoberfest 2026
Building **EXORCIST.EXE** demonstrated that games are one of the most powerful mediums to showcase AI innovation. Instead of another generic chatbot, we created a living, breathing software forensic universe where operating system daemons have personalities, flaws, and secrets.

Don't let your code become a ghost in the machine. Keep your models open, your inference local, and your sockets monitored.

Happy Hacktoberfest! 🎃👻
