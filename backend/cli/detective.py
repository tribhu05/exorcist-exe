#!/usr/bin/env python3
"""
EXORCIST.EXE - Cyber Noir OS Murder Mystery CLI
"The Ghost in the Machine."
Hacktoberfest 2026 Week 4
"""
import sys
import os
import asyncio
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.services.game_engine import game_engine
from app.models.game_schemas import IndictmentRequest

C_GREEN = "\033[92m"
C_AMBER = "\033[93m"
C_RED = "\033[91m"
C_CYAN = "\033[96m"
C_MUTED = "\033[90m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"

DETECTIVE_BANNER = r"""
  ______   _____   _____   _____ _____ _____ _______   ________   ________ 
 |  ____| \ \ / / / ____| / ____|_   _/ ____|__   __| |  ____\ \ / /  ____|
 | |__   __\ V / | |     | (___   | || (___    | |    | |__   \ V /| |__   
 |  __| |___> <  | |      \___ \  | | \___ \   | |    |  __|   > < |  __|  
 | |____   / . \ | |____  ____) |_| |_|___) |  | | _  | |____ / . \| |____ 
 |______| /_/ \_\ \_____|_____/|_____|_____/   |_|(_) |______/_/ \_\______|
  >> CYBER-NOIR OS FORENSICS << CASE #1031: THE MURDER OF PID 1
"""

def slow_print(text: str, delay: float = 0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_banner():
    print(C_GREEN + DETECTIVE_BANNER + C_RESET)

def view_evidence(dossier):
    while True:
        print(f"\n{C_BOLD}{C_CYAN}--- FORENSIC EVIDENCE LOCKER ---{C_RESET}")
        for idx, item in enumerate(dossier.evidence_locker, 1):
            print(f"[{idx}] {item.title} ({C_AMBER}{item.badge}{C_RESET}) - {item.file_path}")
        print("[0] Return to Main Console")

        choice = input(f"\n{C_BOLD}Select evidence file to inspect [0-4]: {C_RESET}").strip()
        if choice == "0":
            break
        try:
            selected_idx = int(choice) - 1
            if 0 <= selected_idx < len(dossier.evidence_locker):
                item = dossier.evidence_locker[selected_idx]
                print(f"\n{C_BOLD}{C_GREEN}=== {item.title} ({item.file_path}) ==={C_RESET}")
                print(f"{C_MUTED}{item.description}{C_RESET}\n")
                print(f"{C_AMBER}FORENSIC HINT:{C_RESET} {item.forensic_hint}\n")
                print(f"{C_MUTED}RAW CONTENTS:{C_RESET}")
                print(item.raw_content)
                input(f"\n{C_BOLD}Press Enter to return to Evidence Locker...{C_RESET}")
        except ValueError:
            pass

async def interrogate_suspects(dossier):
    while True:
        print(f"\n{C_BOLD}{C_CYAN}--- INTERROGATION ROOM: SUSPECTS IN CUSTODY ---{C_RESET}")
        for idx, s in enumerate(dossier.suspects, 1):
            print(f"[{idx}] {s.name} - {C_AMBER}{s.role_title}{C_RESET} ({s.status})")
        print("[0] Return to Main Console")

        choice = input(f"\n{C_BOLD}Select suspect to interrogate [0-4]: {C_RESET}").strip()
        if choice == "0":
            break

        try:
            s_idx = int(choice) - 1
            if 0 <= s_idx < len(dossier.suspects):
                suspect = dossier.suspects[s_idx]
                print(f"\n{C_GREEN}{suspect.avatar_ascii}{C_RESET}")
                print(f"{C_BOLD}{suspect.name}{C_RESET} sits across from you in the interrogation booth.")
                print(f"{C_MUTED}\"{suspect.tagline}\"{C_RESET}")
                print(f"Alibi: {suspect.alibi}\n")

                while True:
                    print(f"\n{C_BOLD}{C_CYAN}[Interrogating {suspect.name}]{C_RESET}")
                    print("Options: Type your question, or enter '/evidence' to present a clue, or '/back' to choose another suspect.")
                    q = input(f"{C_BOLD}Detective Ray Trace > {C_RESET}").strip()

                    if not q:
                        continue
                    if q.lower() == "/back":
                        break

                    evidence_id = None
                    if q.lower() == "/evidence":
                        print("\nSelect evidence to present:")
                        for e_idx, e in enumerate(dossier.evidence_locker, 1):
                            print(f"  ({e_idx}) {e.title}")
                        e_choice = input("Enter clue number [1-4]: ").strip()
                        try:
                            selected_e_idx = int(e_choice) - 1
                            if 0 <= selected_e_idx < len(dossier.evidence_locker):
                                evidence_id = dossier.evidence_locker[selected_e_idx].id
                                print(f"{C_AMBER}[Confronting suspect with {dossier.evidence_locker[selected_e_idx].title}]{C_RESET}")
                                q = "Explain this evidence found at the crime scene!"
                        except ValueError:
                            continue

                    print(f"{C_MUTED}[Awaiting process response...] {C_RESET}")
                    res = await game_engine.interrogate(
                        suspect_id=suspect.id,
                        message=q,
                        presented_evidence_id=evidence_id
                    )

                    tension_bar = "█" * (res.tension_level // 10) + "░" * (10 - res.tension_level // 10)
                    t_color = C_GREEN if res.tension_level < 40 else (C_AMBER if res.tension_level < 75 else C_RED)
                    print(f"\nTension: [{t_color}{tension_bar}{C_RESET}] ({res.tension_level}%)")

                    print(f"\n{C_BOLD}{suspect.name}:{C_RESET}")
                    slow_print(f"\"{res.reply}\"")

                    if res.revealed_clue:
                        print(f"\n{C_RED}[!] CRITICAL REVELATION:{C_RESET} {res.revealed_clue}")

        except ValueError:
            pass

def submit_indictment(dossier):
    print(f"\n{C_BOLD}{C_RED}===================================================={C_RESET}")
    print(f"{C_BOLD}{C_RED}       FORMAL INDICTMENT & EXORCISM TERMINAL         {C_RESET}")
    print(f"{C_BOLD}{C_RED}===================================================={C_RESET}")
    print(f"{C_MUTED}The hardware watchdog timer is ticking. You must name the killer,{C_RESET}")
    print(f"{C_MUTED}identify the murder mechanism, and execute the exorcism command.{C_RESET}\n")

    print(f"{C_BOLD}Suspects:{C_RESET}")
    for idx, s in enumerate(dossier.suspects, 1):
        print(f"  [{idx}] {s.name} ({s.id})")

    s_choice = input(f"\n{C_BOLD}Enter number of accused killer [1-4]: {C_RESET}").strip()
    try:
        s_idx = int(s_choice) - 1
        if 0 <= s_idx < len(dossier.suspects):
            accused_id = dossier.suspects[s_idx].id
        else:
            print("Invalid suspect number.")
            return
    except ValueError:
        return

    weapon = input(f"{C_BOLD}Murder Mechanism / Weapon (e.g. Buffer Overflow, Memory Leak, Fork Bomb): {C_RESET}").strip()
    exorcism_cmd = input(f"{C_BOLD}Exorcism Terminal Command (e.g. kill -9 666, sysctl): {C_RESET}").strip()

    print(f"\n{C_MUTED}[Executing indictment protocol...] {C_RESET}\n")
    time.sleep(1.0)

    req = IndictmentRequest(
        accused_suspect_id=accused_id,
        murder_weapon=weapon,
        exorcism_command=exorcism_cmd
    )
    res = game_engine.evaluate_indictment(req)

    if res.success:
        print(f"{C_BOLD}{C_GREEN}★★★ {res.title} ★★★{C_RESET}")
        print(f"Score: {C_BOLD}{res.score}/100{C_RESET} | Rank: {C_AMBER}{res.detective_rank}{C_RESET}\n")
        slow_print(res.narrative)
        print(f"\n{C_BOLD}Forensic Evaluation:{C_RESET}")
        for k, v in res.breakdown.items():
            print(f"  • {k}: {C_GREEN}{v}{C_RESET}")
    else:
        print(f"{C_BOLD}{C_RED}☠☠☠ {res.title} ☠☠☠{C_RESET}")
        print(f"Score: {C_BOLD}{res.score}/100{C_RESET} | Rank: {C_RED}{res.detective_rank}{C_RESET}\n")
        slow_print(res.narrative)
        print(f"\n{C_BOLD}Forensic Failure Breakdown:{C_RESET}")
        for k, v in res.breakdown.items():
            print(f"  • {k}: {C_RED}{v}{C_RESET}")

async def main():
    print_banner()
    dossier = game_engine.get_dossier()

    print(f"{C_BOLD}CASE BRIEFING:{C_RESET} {dossier.case_number} - {dossier.case_title}")
    print(f"Victim: {C_RED}{dossier.victim}{C_RESET} | Time of Death: {C_AMBER}{dossier.time_of_death}{C_RESET}")
    print(f"\n{C_MUTED}{dossier.briefing}{C_RESET}\n")

    while True:
        print(f"\n{C_BOLD}{C_GREEN}=== DETECTIVE RAY TRACE'S COMMAND DECK ==={C_RESET}")
        print("[1] Inspect Forensic Evidence Locker")
        print("[2] Enter Interrogation Chamber")
        print("[3] Submit Formal Indictment & Exorcise")
        print("[4] Airgap & Open-Source AI Architecture Info")
        print("[0] Exit Game")

        choice = input(f"\n{C_BOLD}Command Deck > {C_RESET}").strip()
        if choice == "1":
            view_evidence(dossier)
        elif choice == "2":
            await interrogate_suspects(dossier)
        elif choice == "3":
            submit_indictment(dossier)
        elif choice == "4":
            print(f"\n{C_BOLD}{C_CYAN}--- AIRGAP & OPEN-SOURCE AI GUARANTEE ---{C_RESET}")
            print("• 100% Local Inference (Ollama with Gemma 2 / Llama 3.2, with built-in offline fallback).")
            print("• Zero external telemetry: no code or prompts leave your machine.")
            print("• Hacktoberfest 2026 Week 4: 'Ghost in the Machine' Official Submission.")
            input("\nPress Enter to return...")
        elif choice == "0":
            print(f"\n{C_MUTED}Leaving the crime scene. Keep watching the sockets, Coroner.{C_RESET}")
            break

if __name__ == "__main__":
    asyncio.run(main())
