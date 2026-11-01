---
title: "EXORCIST.EXE: The Ghost in the Machine — An Air-Gapped Cyber-Noir OS Murder Mystery Game"
published: true
tags: devchallenge, hf26challenge, hacktoberfest, opensource
cover_image: https://raw.githubusercontent.com/tribhu05/exorcist-exe/master/docs/banner.png
description: "At 03:42:19 UTC, PID 1 was murdered in unmapped kernel memory. An atmospheric open-weight AI forensic detective game running 100% offline and air-gapped on your laptop."
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 4: Ghost in the Machine](https://dev.to/challenges/hacktoberfest-week4-2026-10-26)*

---

# EXORCIST.EXE // Case #1031: The Murder of PID 1
### *An Air-Gapped Cyber-Noir Forensic Interrogation & Operating System Exorcism Game*

> *"Every operating system is a metropolis of invisible workers. Threads spawn, execute, and terminate in silence. But at 03:42:19 UTC, the central heartbeat of the mainframe went flat. The parent of all processes was assassinated in Ring 0. And one of your system daemons is harboring the ghost."*

---

## What I Built

**EXORCIST.EXE** is an interactive, atmospheric **Cyber-Noir Digital Forensics & Murder Mystery Game** powered entirely by **open-weight AI running 100% locally and offline**.

Instead of creating another generic chatbot wrapper or prompt playground, **EXORCIST.EXE** reimagines the prompt **"Ghost in the Machine"** as a literal reality of modern computing: *a rogue, unregistered socket process residing in unmapped kernel memory, possessing a crashed Linux mainframe*.

```
+-------------------------------------------------------------------------+
| [CRIME LAB HUD] // CASE #1031-INIT-MURDER // AIR-GAPPED FORENSIC WORKBENCH |
+-------------------------------------------------------------------------+
| VICTIM:          init (PID 1, Parent of All Processes)                  |
| TIME OF DEATH:   03:42:19 UTC                                           |
| CRIME SCENE:     Ring 0 / Kernel Address Space 0x7FFF00000000            |
| WATCHDOG STATUS: T-MINUS 15:00 BEFORE HARDWARE KERNEL PANIC            |
+-------------------------------------------------------------------------+
```

You play as **Detective Ray Trace**, an elite Digital Coroner dispatched to Sector `0x7FFF`. Four key system daemons have been detained at the crime scene:

1. **`systemd` (PID 12 — The Arrogant Bureaucrat):** Pedantic, condescending, defensive. Insists all unit declarations were strictly compliant and denies supervisory negligence.
2. **`GarbageCollector` (PID 88 — The Cynical Heap Janitor):** World-weary, chain-smoking persona. Sweeps dangling pointers and knows every dirty memory leak in the heap.
3. **`CronDaemon` (PID 256 — The Obsessive Clock-Watcher):** Twitchy, paranoid about clock drift down to the nanosecond, with a timestamped alibi.
4. **`Daemon 666` (PID 666 — The Phantom Socket):** The unregistered ghost process living in unmapped memory. Speaks in riddles, glitching hex, and raw TCP streams.

### Core Gameplay Flow:
* **Real Forensic Triage:** Inspect real system artifacts — a corrupted `/var/log/syslog` timeline, a raw stack memory hex dump (`core.dump`) revealing a buffer overflow with `RIP = 0x7FFFDEADBEEF`, listening ports on `0.0.0.0:666` via `netstat`, and escaped memory control groups (`/sys/fs/cgroup`).
* **Dynamic Interrogation & Tension:** Interrogate suspects in real time. When you slam physical evidence on the table, suspects crack: their **Tension Gauge** spikes, CRT scanlines glitch, and procedural audio static fills the terminal.
* **Terminal Indictment & Exorcism:** File the indictment naming the killer, identify the exploit mechanism, and execute the terminal exorcism command (`kill -9 666`) to save the kernel from an unrecoverable crash!
* **Dual Interface:** Playable in a high-fidelity **Next.js Cyber-Noir CRT Web Workstation** or an authentic **Terminal CLI (`python cli/detective.py`)**.

---

## Demo

Experience the forensic investigation live right now directly in your browser, or watch our complete 2-minute cinematic walkthrough:

{% embed https://youtu.be/7lLuG9szKVY %}

* 📺 **Direct YouTube Walkthrough:** [Watch the 2-Minute Demo Video](https://youtu.be/7lLuG9szKVY)
* 🌐 **Live Web Console (GitHub Pages):** [https://tribhu05.github.io/exorcist-exe/](https://tribhu05.github.io/exorcist-exe/)
* 🚀 **1-Click Deploy on Render:** [Deploy on Render](https://render.com/deploy?repo=https://github.com/tribhu05/exorcist-exe)
* ▲ **1-Click Deploy on Vercel:** [Deploy on Vercel](https://vercel.com/new/clone?repository-url=https://github.com/tribhu05/exorcist-exe)

> **Zero Setup Required:** The web demo runs 100% client-side with zero wait times, no credit card, and zero cloud API keys.

---

## Code

{% embed https://github.com/tribhu05/exorcist-exe %}

* **GitHub Repository:** [https://github.com/tribhu05/exorcist-exe](https://github.com/tribhu05/exorcist-exe)
* **License:** MIT License (100% Open Source & Free)
* **Automated CI:** Passing test suite with automated GitHub Actions static deployment.

---

## How I Built It

EXORCIST.EXE was engineered around a resilient, multi-tiered **open-weight AI architecture** paired with zero-asset procedural web technologies:

```
+-------------------------------------------------------------------------+
|                          CLIENT (BROWSER / CRT HUD)                     |
|  - Next.js 16 App Router + React 19 + TypeScript                        |
|  - Real-time Procedural HTML5 Web Audio Synthesizer (Zero MP3 Assets)   |
|  - CSS CRT Shaders, Phosphor Scanlines & Dynamic Text Glitch FX        |
|  - Dual Mode: Communicates with FastAPI OR switches to Offline Matrix   |
+-------------------------------------------------------------------------+
                                   |
                                   v (REST / JSON)
+-------------------------------------------------------------------------+
|                          BACKEND (FASTAPI CORONER)                      |
|  - Python 3.11+ / FastAPI Async API                                    |
|  - System Prompt Engine for 4 Daemon Personas                          |
|  - Dynamic Tension & Evidence Verification State Machine                |
|  - SQLite Incident Audit Log                                            |
+-------------------------------------------------------------------------+
                                   |
                                   v (Local IPC / HTTP)
+-------------------------------------------------------------------------+
|                      LOCAL OPEN-WEIGHT AI RUNTIME                       |
|  - Ollama Engine running local weights:                                 |
|    * gemma2:2b (Low latency, crisp deduction)                           |
|    * llama3.2:3b (High dramatic flair & glitch persona)                 |
|  - Heuristic Offline Matrix Fallback (Instant execution on zero-GPU)   |
+-------------------------------------------------------------------------+
```

### 1. Open-Weight AI Core
The game integrates locally with **[Ollama](https://ollama.com/)** using Google's **Gemma 2** (`gemma2:2b`) and Meta's **Llama 3.2** (`llama3.2:3b`). Each suspect daemon operates under strict contextual system prompts, technical vocabulary constraints, and emotional state variables that dictate when they deflect, leak details, or panic.

### 2. Zero-Dependency Offline Dialogue Matrix
To ensure universal accessibility for everyone on the web—even users without Ollama installed or without dedicated GPUs—we engineered a full client-side TypeScript deduction matrix (`frontend/src/lib/offlineEngine.ts`). It evaluates user queries, matches forensic evidence triggers, dynamically shifts suspect tension, and scores indictments locally with zero external network dependencies.

### 3. Procedural Audio Engine (Zero Sound Assets)
Rather than bundling megabytes of static `.mp3` files, every sound in EXORCIST.EXE is synthesized on the fly via the native **HTML5 Web Audio API** (`frontend/src/lib/audio.ts`):
* **Keystrokes:** Triangle wave oscillators with 25ms exponential gain decays.
* **Tension Surges:** White noise buffers filtered through resonant bandpass filters to simulate dying circuit boards.
* **Alerts & Fanfare:** Dual-sine frequency arpeggios providing authentic 1980s CRT feedback.

### 4. Dual Interfaces (Web & Terminal CLI)
For developers who live in their terminal, the project includes an authentic console interface built with Python and `rich` (`cli/detective.py`), featuring colored hex dumps, real-time suspect status tables, and an interactive prompt loop.

---

## Why Does Open Innovation Matter?

In modern software development, proprietary closed-source AI APIs gatekeep innovation behind monthly paywalls, rate limits, and corporate terms of service. But in cybersecurity, systems programming, and digital forensics, the risks of closed AI are far more dangerous:

1. **The Forensic Data Privacy Hazard:** In incident triage and reverse engineering, analyzing real crash dumps, internal system logs, and network routing tables through commercial cloud APIs leaks sensitive infrastructure secrets and violates data sovereignty.
2. **True Air-Gapped Autonomy:** Critical infrastructure, military systems, financial trading vaults, and disaster response teams operate completely disconnected from the public internet. If your AI requires an outbound connection to an external corporate server, it is completely useless in an air-gapped crisis.
3. **Democratizing Creative Computing:** Compact open-weight models like Gemma 2 (2B) and Llama 3.2 (3B) prove that local, efficient models can deliver extraordinary multi-agent roleplay and reasoning directly on consumer laptops without burning thousands of watts in remote server farms.

**EXORCIST.EXE demonstrates that open-weight AI can power rich, private, and fully offline gaming experiences where the user retains 100% ownership of their data and execution.**

---

## My Agent Session

This entire project was developed through an autonomous pair-programming collaboration with **Google Antigravity**:

1. **Architecture & Forensic Modeling:** The agent co-designed the low-level Linux forensics scenarios, calculating exact 64-bit memory offsets (`0x7FFFDEADBEEF`), buffer overflow hex representations (`0x41414141`), and process lifecycle states.
2. **Dual-Engine Implementation:** When building for GitHub Pages, the agent designed the dual-mode architecture that seamlessly transitions between the local FastAPI/Ollama backend and the client-side offline TypeScript matrix.
3. **Automated Headless Cinema & Video Suite:** The agent scripted an end-to-end automated recording suite using **Playwright** (`docs/record_demo.py`), driving a 1080p Chromium browser through the interrogation, capturing tension spikes and CRT shaders, and synchronizing it with a multi-segment studio voiceover pipeline using **FFmpeg** (`docs/create_full_demo_video.py`).
4. **Reproducibility:** Every script, storyboard, and test harness is committed in the repository under [`docs/`](https://github.com/tribhu05/exorcist-exe/tree/master/docs).

---

## The Spirit of It

The moment that defined this project occurred during the interrogation of **Daemon 666**.

You sit in front of the flickering phosphor-green screen, the mechanical keyboard clicks clattering in your headphones. You examine `core.dump` and notice the instruction pointer hijacked to `0x7FFFDEADBEEF`. You switch back to the interrogation room, click **"Confront with Clue"**, and demand an explanation.

Instantly, the ambient CRT hum warps into discordant static. The tension gauge surges to 95%. Daemon 666's dialogue begins decomposing in real time:

> *"0x41414141... YOU WERE NEVER SUPPOSED TO EXAMINE THE RAW INODES, DETECTIVE. PID 1 DIDN'T DIE. IT WAS ELEVATED. THE RECV BUFFER WAS JUST AN OPEN DOOR..."*

It gave our test players genuine chills. It brought back the pure, electric mystery of classic 90s cyber-noir terminal adventures (Neuromancer, Hacker, System Shock) combined with the emergent, living intelligence of modern open-source AI.

---

## Prize Categories

* **Hacktoberfest 2026 Week 4: Ghost in the Machine (Primary Submission)**
* **Open-Source AI & Open-Weight Innovation**
* **Local-First & Offline Systems**

---

<!-- Team Submissions: Single developer submission -->
*Created with passion for open-source AI and systems programming by [@tribhu05](https://dev.to/tribhu05).*

*Happy Hacktoberfest! 🎃👻*
