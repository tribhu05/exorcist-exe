#!/usr/bin/env python3
"""
PHANTOM//SHELL CLI Daemon
"The Ghost in your Terminal."
"""
import sys
import os
import asyncio
import subprocess
import argparse
from typing import List

# Ensure app package is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.services.llm_engine import llm_engine
from app.services.grimoire_store import grimoire_store
from app.config import settings

SPECTRAL_BANNER = r"""
  ____  _   _    _    _   _ _____ ___  __  __   //   ____  _   _ _____ _     _     
 |  _ \| | | |  / \  | \ | |_   _/ _ \|  \/  | //   / ___|| | | | ____| |   | |    
 | |_) | |_| | / _ \ |  \| | | || | | | |\/| |//    \___ \| |_| |  _| | |   | |    
 |  __/|  _  |/ ___ \| |\  | | || |_| | |  | |//     ___) |  _  | |___| |___| |___ 
 |_|   |_| |_/_/   \_\_| \_| |_| \___/|_|  |_|//    |____/|_| |_|_____|_____|_____|
  >> THE GHOST IN YOUR MACHINE << [AIR-GAPPED // ZERO-TELEMETRY]
"""

def print_banner():
    print("\033[92m" + SPECTRAL_BANNER + "\033[0m")

async def cmd_run(args: List[str]):
    if not args:
        print("\033[91mError: No command specified to run.\033[0m")
        sys.exit(1)

    command_str = " ".join(args)
    print(f"\033[90m[phantom]\033[0m Monitoring execution: \033[1m{command_str}\033[0m\n")

    # Run subprocess
    proc = subprocess.Popen(
        command_str,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = proc.communicate()
    exit_code = proc.returncode

    if stdout:
        print(stdout, end="")
    if stderr:
        print("\033[91m" + stderr + "\033[0m", end="")

    if exit_code != 0:
        print_banner()
        print(f"\033[91m[!] SPECTRAL ANOMALY DETECTED (Exit code {exit_code})\033[0m")
        print("\033[90m[-] Engaging open-weight forensic autopsy...\033[0m\n")

        autopsy = await llm_engine.autopsy_command(
            command=command_str,
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            cwd=os.getcwd()
        )

        print(f"\033[1;92mINCIDENT ID:\033[0m      {autopsy.incident_id}")
        print(f"\033[1;93mCLASSIFICATION:\033[0m   {autopsy.ghost_type} [{autopsy.severity}]")
        print(f"\033[1;97mDIAGNOSIS:\033[0m        {autopsy.spectral_diagnosis}")
        print(f"\033[1;97mROOT CAUSE:\033[0m       {autopsy.root_cause}")
        
        if autopsy.suggested_command:
            print(f"\n\033[1;92m[+] EXORCISM COMMAND:\033[0m")
            print(f"    \033[40;1;93m {autopsy.suggested_command} \033[0m")

        print(f"\n\033[90mInference Engine: {autopsy.model_used} | Airgap: VERIFIED OFFLINE\033[0m\n")

        # Record in Grimoire
        grimoire_store.record_incident(
            incident_id=autopsy.incident_id,
            incident_type="CLI_AUTOPSY",
            title=f"{autopsy.ghost_type} ({command_str})",
            severity=autopsy.severity,
            details=autopsy.model_dump()
        )

    sys.exit(exit_code)

async def cmd_scan(file_path: str):
    if not os.path.exists(file_path):
        print(f"\033[91mError: File not found: {file_path}\033[0m")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    print_banner()
    print(f"\033[90m[-] Performing static exorcism scan on:\033[0m \033[1m{file_path}\033[0m\n")

    res = await llm_engine.exorcise_code(
        code=code,
        filename=os.path.basename(file_path),
        language="python" if file_path.endswith(".py") else "javascript"
    )

    color = "\033[92m" if res.haunted_score < 30 else ("\033[93m" if res.haunted_score < 70 else "\033[91m")
    print(f"Haunted Score: {color}{res.haunted_score}/100\033[0m")
    print(f"Summary:       {res.spectral_summary}\n")

    if res.anomalies_found:
        print("\033[1;93mDetected Code Hauntings:\033[0m")
        for anomaly in res.anomalies_found:
            print(f"  • \033[1mLine {anomaly.line_number}\033[0m [{anomaly.severity}] \033[92m{anomaly.ghost_pattern}\033[0m")
            print(f"    \033[90m{anomaly.description}\033[0m")
        
        print("\n\033[1;92mPurification Diff:\033[0m")
        print(res.unified_diff)

async def main():
    parser = argparse.ArgumentParser(description="PHANTOM//SHELL CLI")
    subparsers = parser.add_subparsers(dest="subcommand")

    # Run subcommand
    run_parser = subparsers.add_parser("run", help="Run a command under the Phantom watcher")
    run_parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Command to execute")

    # Scan subcommand
    scan_parser = subparsers.add_parser("scan", help="Scan a file for haunted bugs")
    scan_parser.add_argument("file", help="File to scan")

    # Status subcommand
    subparsers.add_parser("status", help="Inspect Spectre daemon status")

    args = parser.parse_args()

    if args.subcommand == "run":
        await cmd_run(args.cmd)
    elif args.subcommand == "scan":
        await cmd_scan(args.file)
    elif args.subcommand == "status":
        print_banner()
        is_alive = await llm_engine.is_ollama_alive()
        print(f"Model Configured: {settings.OLLAMA_MODEL}")
        print(f"Ollama Endpoint:  {settings.OLLAMA_BASE_URL} [{'ONLINE' if is_alive else 'OFFLINE (Fallback Active)'}]")
        print(f"Grimoire Incidents: {grimoire_store.get_count()} stored in {settings.DB_PATH}")
        print(f"Privacy Guarantee: 100% Local Air-Gapped Inference")
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())
