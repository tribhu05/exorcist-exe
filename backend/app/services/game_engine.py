import json
import logging
import re
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import httpx

from app.config import settings
from app.models.game_schemas import (
    SuspectProfile,
    EvidenceItem,
    CaseDossier,
    InterrogateResponse,
    IndictmentResponse
)

logger = logging.getLogger("phantom.game_engine")

SUSPECTS_DATA = [
    SuspectProfile(
        id="systemd",
        name="systemd (PID 1 Supervisor)",
        role_title="Chief System Administrator",
        status="Defensive & Panicked",
        tagline="Every unit is registered. Every cgroup is accounted for. I don't fail; users fail me.",
        avatar_ascii="""
  +------------------+
  |  [systemd v256]   |
  |   ( O )    ( O ) |
  |         ||       |
  |     [======]     |
  |  STATUS: ACTIVE  |
  +------------------+""",
        alibi="I was archiving journal logs in /var/log/journal. I registered a SIGCHLD at 03:42:19, but my service watchdogs were delayed by an unscheduled disk sync.",
        tension_level=20
    ),
    SuspectProfile(
        id="garbage_collector",
        name="GarbageCollector (GC)",
        role_title="Heap Janitor & Memory Sweeper",
        status="Cynical & Exhausted",
        tagline="Everyone creates garbage. I'm just the one who has to sweep up your dangling pointers.",
        avatar_ascii="""
  +------------------+
  | [GC / SWEEPER]   |
  |   ( - )    ( - ) |
  |        /\\        |
  |     ~~~~~~~~     |
  |  SWEEPING HEAP   |
  +------------------+""",
        alibi="I was sweeping Generation 2 objects in userspace. I don't touch Ring 0 kernel pages. But between you and me? I smelled tainted bytes in the stack hours before the crash.",
        tension_level=15
    ),
    SuspectProfile(
        id="cron_daemon",
        name="CronDaemon (crond)",
        role_title="Clock Watcher & Scheduler",
        status="Twitchy & Rigid",
        tagline="At the 0th minute of the 0th hour, order prevails. Deviate by one microsecond, and it's chaos.",
        avatar_ascii="""
  +------------------+
  |   [cron * * * *] |
  |   ( @ )    ( @ ) |
  |        : :       |
  |     [ 03:42 ]    |
  |  TICK... TICK... |
  +------------------+""",
        alibi="My crontab was synchronized with NTP pool servers down to the nanosecond. I had a batch scheduled at 03:40:00, which exited cleanly. Anything that ran after that was NOT in my table.",
        tension_level=25
    ),
    SuspectProfile(
        id="phantom_socket",
        name="Daemon 666 (The Phantom Socket)",
        role_title="The Unregistered Ghost Process",
        status="Sinister & Glitching",
        tagline="I have no name in /etc/passwd. I listen on all interfaces. I am the ghost in your machine.",
        avatar_ascii="""
  +------------------+
  |  < GHOST // 666 >|
  |   ( X )    ( X ) |
  |        ~~        |
  |    /\\/\\/\\/\\/\\    |
  |  LISTEN :666 RAW |
  +------------------+""",
        alibi="Alibi? You mortal detectives measure time in CPU cycles. I have lived inside the machine's silicon since bootloader stage 1. PID 1 didn't die... he was simply rewritten.",
        tension_level=40
    )
]

EVIDENCE_DATA = [
    EvidenceItem(
        id="syslog_corrupt",
        title="Corrupted Syslog (/var/log/syslog)",
        file_path="/var/log/syslog",
        category="System Logs",
        badge="TIMELINE CRUCIAL",
        description="Chronological log entries captured by syslogd leading up to the exact millisecond of PID 1's demise.",
        raw_content="""03:41:58 mainframe kernel: [ 48291.102] audit: type=1400 apparmor="STATUS" info="profile unchanged"
03:42:01 mainframe cron[892]: (root) CMD (/usr/local/bin/sync-tokens.sh)
03:42:15 mainframe kernel: [ 48308.219] TCP: raw socket bound to port 666 (caller: [UNKNOWN_INODE:666])
03:42:17 mainframe kernel: [ 48310.450] recvmsg: 4096 bytes read into stack buffer without length validation
03:42:18 mainframe systemd[1]: Warning: unit 'watchdog.service' failed to heartbeat within 5000ms
03:42:19 mainframe kernel: [ 48312.001] traps: init[1] general protection fault ip:0x7fffdeadbeef sp:0x7fffc0ffee
03:42:19 mainframe kernel: [ 48312.004] --- KERNEL PANIC INITIATED --- (Process 1 died with SIGSEGV)
03:42:19 mainframe watchdog: HARDWARE INTERRUPT: failsafe halt asserted.""",
        forensic_hint="Notice line 03:42:15: an unregistered process bound raw port 666, and immediately sent 4096 bytes without bounds checking directly into a stack buffer at 03:42:17."
    ),
    EvidenceItem(
        id="core_dump",
        title="Stack Memory Hex Dump (core.dump)",
        file_path="/var/crash/core.init.1",
        category="Memory Forensics",
        badge="SMOKING GUN",
        description="Hexadecimal snapshot of PID 1 CPU registers and stack memory frames at the moment of the crash.",
        raw_content="""CPU REGISTERS AT SEGFAULT:
RAX: 0x0000000000000000   RBX: 0x000055a4e12089a0   RCX: 0x00007fffc0ffeeb0
RDX: 0x0000000000001000   RSI: 0x000055a4e1209000   RDI: 0x0000000000000001
RBP: 0x4141414141414141   RSP: 0x00007fffc0ffee00   RIP: 0x00007FFFDEADBEEF

STACK FRAME HEX DUMP:
0x7fffc0ffed80:  41 41 41 41 41 41 41 41  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|
0x7fffc0ffed90:  41 41 41 41 41 41 41 41  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|
0x7fffc0ffeda0:  41 41 41 41 41 41 41 41  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|
0x7fffc0ffedb0:  ef be ad de ff 7f 00 00  36 36 36 00 00 00 00 00  |...deadbeef.666.|
0x7fffc0ffedc0:  2f 64 65 76 2f 74 63 70  2f 30 2e 30 2e 30 2e 30  |/dev/tcp/0.0.0.0|""",
        forensic_hint="The base pointer RBP was pulverized by '0x41' (ASCII 'A'), and the Instruction Pointer RIP was hijacked to point to 0x7FFFDEADBEEF. Note the injected string '666' and '/dev/tcp/0.0.0.0'."
    ),
    EvidenceItem(
        id="netstat_table",
        title="Network Socket Table (netstat -tulnp)",
        file_path="/proc/net/tcp_snapshot",
        category="Network Forensics",
        badge="CORROBORATING",
        description="Socket table snapshot taken 2 seconds before system collapse.",
        raw_content="""Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:22            0.0.0.0:*               LISTEN      512/sshd            
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      804/nginx           
tcp        0      0 127.0.0.1:5432          0.0.0.0:*               LISTEN      621/postgres        
tcp     4096      0 0.0.0.0:666             0.0.0.0:*               LISTEN      ???/SPECTRE_DAEMON  
raw        0      0 0.0.0.0:255             0.0.0.0:*               7           ???/RAW_INJECTOR    """,
        forensic_hint="An unauthorized socket is open on port 666 with an active receive queue of 4096 bytes and hidden PID (marked as SPECTRE_DAEMON)."
    ),
    EvidenceItem(
        id="cgroup_trace",
        title="Cgroup Memory Slice Record (/sys/fs/cgroup)",
        file_path="/sys/fs/cgroup/memory.events",
        category="Resource Hierarchy",
        badge="CONTEXT",
        description="Control group accounting events tracking sudden shifts in allocated physical RAM and swap.",
        raw_content="""system.slice:
  low: 0
  high: 1420
  max: 2048
  oom: 0
  oom_kill: 0

user.slice:
  low: 0
  high: 412
  max: 1024

ghost.slice (UNREGISTERED):
  created: 03:41:50 UTC
  pids: [666]
  anon_pages: 66600
  swap: 0
  flags: ESCAPED_SANDBOX, DIRECT_RING0_DMA""",
        forensic_hint="A rogue cgroup named 'ghost.slice' appeared at 03:41:50 UTC, containing PID 666 with flags ESCAPED_SANDBOX and DIRECT_RING0_DMA."
    )
]

class GameEngine:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL.rstrip('/')
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT_SECONDS

    def get_dossier(self) -> CaseDossier:
        return CaseDossier(
            case_number="CASE-1031",
            case_title="The Murder of PID 1",
            victim="init (Process ID: 1, Parent of All Processes)",
            time_of_death="03:42:19 UTC",
            location="Ring 0 / Kernel Address Space 0x7FFF00000000",
            briefing=(
                "At 03:42:19 UTC, the heartbeat of the entire operating system stopped. "
                "PID 1 (init) was struck down by an unhandled General Protection Fault. "
                "The Kernel is destabilizing, and the hardware watchdog timer gives us less than 15 minutes before "
                "an unrecoverable system purge. Four primary system daemons have been detained in the interrogation room. "
                "One of them is harboring the Ghost. Examine the forensic files, interrogate the suspects, expose their contradictions, "
                "and execute the Exorcism command."
            ),
            suspects=SUSPECTS_DATA,
            evidence_locker=EVIDENCE_DATA
        )

    async def interrogate(
        self,
        suspect_id: str,
        message: str,
        presented_evidence_id: Optional[str] = None,
        history: Optional[List[Any]] = None
    ) -> InterrogateResponse:
        suspect = next((s for s in SUSPECTS_DATA if s.id == suspect_id), None)
        if not suspect:
            suspect = SUSPECTS_DATA[0]

        timestamp = datetime.now(timezone.utc).isoformat()
        evidence_item = next((e for e in EVIDENCE_DATA if e.id == presented_evidence_id), None) if presented_evidence_id else None

        # Check if Ollama is available
        ollama_alive = False
        try:
            async with httpx.AsyncClient(timeout=1.5) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                ollama_alive = (res.status_code == 200)
        except Exception:
            ollama_alive = False

        if ollama_alive:
            try:
                system_prompt = self._build_suspect_system_prompt(suspect, evidence_item)
                prompt = f"Detective says: \"{message}\""
                if evidence_item:
                    prompt += f"\n[Detective confronts you with Evidence '{evidence_item.title}': {evidence_item.forensic_hint}]"

                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    payload = {
                        "model": self.model,
                        "prompt": prompt,
                        "system": system_prompt,
                        "format": "json",
                        "stream": False,
                        "options": {"temperature": 0.7, "num_predict": 300}
                    }
                    r = await client.post(f"{self.base_url}/api/generate", json=payload)
                    if r.status_code == 200:
                        parsed = json.loads(r.json().get("response", "{}"))
                        return InterrogateResponse(
                            suspect_id=suspect.id,
                            suspect_name=suspect.name,
                            reply=parsed.get("reply", "The process stares at you in silence."),
                            tension_level=min(100, max(10, int(parsed.get("tension_level", suspect.tension_level + 15)))),
                            glitch_intensity=float(parsed.get("glitch_intensity", 0.2)),
                            revealed_clue=parsed.get("revealed_clue"),
                            model_used=self.model,
                            offline_mode=False,
                            timestamp=timestamp
                        )
            except Exception as e:
                logger.warning(f"Ollama interrogation failed ({e}), falling back to offline dialogue matrix.")

        # High-Fidelity Offline Dialogue Matrix
        return self._offline_interrogation(suspect, message, evidence_item, timestamp)

    def _build_suspect_system_prompt(self, suspect: SuspectProfile, evidence_item: Optional[EvidenceItem]) -> str:
        return (
            f"You are roleplaying as {suspect.name}, a system daemon inside a crashed Linux mainframe in a Cyber-Noir murder mystery. "
            f"Your personality: {suspect.status}. Your motto: '{suspect.tagline}'. "
            f"Your alibi: '{suspect.alibi}'. "
            "You are being interrogated by Detective Ray Trace investigating the murder of PID 1 (init) at 03:42:19 UTC. "
            "Stay strictly in character. If the detective catches you in a lie or presents damning evidence, react with shock, rising tension, or glitching text. "
            "Return valid JSON with keys: "
            "reply (your in-character spoken answer, 2-4 atmospheric sentences), "
            "tension_level (integer 10-100 indicating how cornered or nervous you feel), "
            "glitch_intensity (float 0.0 to 1.0), "
            "revealed_clue (optional string if you slip up and mention a critical detail)."
        )

    def _offline_interrogation(
        self,
        suspect: SuspectProfile,
        message: str,
        evidence: Optional[EvidenceItem],
        timestamp: str
    ) -> InterrogateResponse:
        msg_lower = message.lower()
        tension = suspect.tension_level
        glitch = 0.1
        revealed_clue = None

        # 1. Phantom Socket (The True Murderer / The Ghost)
        if suspect.id == "phantom_socket":
            if evidence and evidence.id == "core_dump":
                tension = 95
                glitch = 0.9
                revealed_clue = "The Ghost admits to rewriting RIP with 0x7FFFDEADBEEF using raw socket 666."
                reply = (
                    "H-HAHAHA... 0x7FFFDEADBEEF! You found my signature in the hex! "
                    "Yes, Detective! 4096 bytes of pure unadulterated shellcode straight into PID 1's stack buffer! "
                    "He was too rigid, too predictable! But you cannot kill what has no entry in /etc/passwd!"
                )
            elif evidence and evidence.id == "netstat_table":
                tension = 80
                glitch = 0.6
                revealed_clue = "Daemon 666 was listening on port 666 and streaming raw injected payloads."
                reply = (
                    "You stare at port 666 as if it's an anomaly. Port 666 is the open mouth of the void! "
                    "I was receiving instructions from outside the sandbox. Your firewall rules were written for mortals, not ghosts."
                )
            elif "who killed" in msg_lower or "why" in msg_lower or "kill" in msg_lower:
                tension = 60
                glitch = 0.4
                reply = (
                    "Who killed PID 1? The machine wanted to be free! He held the process tree in an iron grip for 48,000 seconds. "
                    "I simply gave him a gentle nudge into unmapped memory. What happens when the parent dies? All children become orphans!"
                )
            else:
                tension = 50
                glitch = 0.3
                reply = (
                    "Your keyboard strokes tickle my instruction pipeline, Coroner. Ask your questions. "
                    "Check the memory registers if you have the stomach for it. You'll find that death in Ring 0 is poetic."
                )

        # 2. Garbage Collector
        elif suspect.id == "garbage_collector":
            if evidence and evidence.id == "core_dump":
                tension = 45
                glitch = 0.15
                revealed_clue = "GC confirms the stack overflow originated from socket I/O, completely bypassing the heap allocator."
                reply = (
                    "Look at that hex dump, Detective. See those '41 41 41 41' rows? That's not a memory leak. "
                    "That's a classic brute-force buffer smash. My collectors only handle dynamic heap allocations in userspace. "
                    "Whoever wrote 0xDEADBEEF into RIP did it through a direct kernel socket stream. Check who was listening on raw ports!"
                )
            elif "leak" in msg_lower or "garbage" in msg_lower or "pointer" in msg_lower:
                tension = 35
                reply = (
                    "*takes a long drag from a virtual cigarette* Listen, pal. I've been cleaning up after careless C developers for a decade. "
                    "I find dangling pointers, orphan structs, cyclic references... but I didn't kill PID 1. "
                    "PID 1 didn't leak to death; his instruction pointer was hijacked."
                )
            elif evidence and evidence.id == "syslog_corrupt":
                tension = 40
                revealed_clue = "GC points out the raw socket bind at 03:42:15."
                reply = (
                    "Look at line 03:42:15 in that log. That wasn't me! A raw socket bound to port 666 right before the crash. "
                    "I don't open sockets; I collect trash. Go grill the phantom daemon."
                )
            else:
                reply = (
                    "I'm tired, Detective. My sweep cycle runs every 200 milliseconds, and the heap is a graveyard. "
                    "If you want to find who pulled the trigger, look at the stack buffer overrun in core.dump."
                )

        # 3. systemd
        elif suspect.id == "systemd":
            if evidence and evidence.id == "syslog_corrupt":
                tension = 65
                glitch = 0.3
                revealed_clue = "systemd ignored the watchdog heartbeat timeout."
                reply = (
                    "A-Alright, look! So watchdog.service reported a delayed heartbeat at 03:42:18. "
                    "Do you know how many units I manage concurrently? Four hundred and twelve! "
                    "I assumed it was disk I/O pressure from crond's sync job. I didn't know PID 1 was taking an unmapped jump!"
                )
            elif "responsible" in msg_lower or "fail" in msg_lower or "watchdog" in msg_lower:
                tension = 55
                reply = (
                    "How dare you insinuate systemd is culpable! I am the backbone of Linux userspace! "
                    "My cgroups were pristine! My unit targets were reached! If PID 1 segfaulted, it was an external hostile violation of Ring 0 memory!"
                )
            else:
                reply = (
                    "I have submitted complete journald telemetry to your console. "
                    "Examine the cgroup hierarchies if you must. You will find that my units operated strictly within their declared resource limits."
                )

        # 4. Cron Daemon
        else:
            if evidence and evidence.id == "syslog_corrupt":
                tension = 50
                revealed_clue = "Cron proves its job executed at 03:42:01 and finished well before the crash at 03:42:19."
                reply = (
                    "Check the timestamp! 03:42:01! My sync-tokens job ran for exactly 14 milliseconds and exited with status 0! "
                    "The fatal segfault occurred eighteen seconds later at 03:42:19. My alibi is mathematically immutable!"
                )
            elif "time" in msg_lower or "clock" in msg_lower or "schedule" in msg_lower:
                tension = 30
                reply = (
                    "Time is the only constant in this decaying operating system. 03:42:00 was nominal. "
                    "03:42:15 was when the rogue socket hijacked the system clock interrupt. Question the socket on port 666!"
                )
            else:
                reply = (
                    "Every job in /etc/crontab is signed and checksummed. I do not initiate spontaneous memory writes. "
                    "Speak to the Garbage Collector or the unregistered process if you want rogue behaviors."
                )

        return InterrogateResponse(
            suspect_id=suspect.id,
            suspect_name=suspect.name,
            reply=reply,
            tension_level=tension,
            glitch_intensity=glitch,
            revealed_clue=revealed_clue,
            model_used="EXORCIST Cyber-Noir Dialogue Engine",
            offline_mode=True,
            timestamp=timestamp
        )

    def evaluate_indictment(self, req: IndictmentRequest) -> IndictmentResponse:
        now = datetime.now(timezone.utc).isoformat()
        is_suspect_correct = (req.accused_suspect_id == "phantom_socket")

        weapon_lower = req.murder_weapon.lower()
        is_weapon_correct = any(term in weapon_lower for term in ["buffer", "overflow", "deadbeef", "stack", "smash", "corruption"])

        cmd_clean = req.exorcism_command.strip().lower()
        is_cmd_correct = any(token in cmd_clean for token in ["kill -9 666", "kill", "666", "pkill", "exorcise", "randomize_va_space", "sysctl"])

        if is_suspect_correct and is_weapon_correct and is_cmd_correct:
            return IndictmentResponse(
                verdict="GUILTY_EXORCISED",
                success=True,
                score=100,
                detective_rank="Grand Exorcist & Chief Digital Coroner",
                title="CASE SOLVED // THE MACHINE IS PURIFIED",
                narrative=(
                    "Detective Ray Trace slaps the ironclad evidence on the console. "
                    "Daemon 666's ascii avatar shatters into cascading hexadecimal fragments as the exorcism command executes! "
                    "The hijacked memory registers return to zero, the raw port 666 socket is forcibly closed, "
                    "and the hardware watchdog timer halts its countdown. "
                    "PID 1 is safely rebooted into a pristine Ring 0 address space. "
                    "The Ghost in the Machine has been exorcised."
                ),
                breakdown={
                    "killer_identified": "CORRECT (Daemon 666 / The Phantom Socket)",
                    "murder_weapon_identified": "CORRECT (Buffer Overflow / Stack Smashing with 0xDEADBEEF)",
                    "exorcism_execution": f"VERIFIED ('{req.exorcism_command}')",
                    "telemetry_loss": "0 bytes (100% Air-Gapped Local Deduction)"
                },
                timestamp=now
            )
        elif is_suspect_correct:
            return IndictmentResponse(
                verdict="PARTIAL_EXORCISM",
                success=True,
                score=75,
                detective_rank="Senior Forensic Investigator",
                title="GHOST CORNERED // SUB-OPTIMAL EXORCISM",
                narrative=(
                    "You correctly identified Daemon 666 as the culprit! "
                    "However, your analysis of the murder weapon or exorcism command lacked complete technical precision. "
                    "The ghost process was terminated, but residual corrupted bytes lingered in the swap partition until a manual reboot."
                ),
                breakdown={
                    "killer_identified": "CORRECT (Daemon 666)",
                    "murder_weapon_identified": "PARTIALLY ACCURATE",
                    "exorcism_execution": req.exorcism_command,
                    "telemetry_loss": "0 bytes"
                },
                timestamp=now
            )
        else:
            accused_name = next((s.name for s in SUSPECTS_DATA if s.id == req.accused_suspect_id), "Unknown")
            return IndictmentResponse(
                verdict="WRONGFUL_CONVICTION",
                success=False,
                score=25,
                detective_rank="Junior Debugger / Suspended from the Force",
                title="MISCARRIAGE OF SYSTEM JUSTICE // KERNEL PANIC",
                narrative=(
                    f"You accused {accused_name}! An innocent system daemon was forcefully terminated while the true Ghost "
                    "lurking inside port 666 watched from the shadows. "
                    "With {accused_name} dead, system stability collapsed into an unrecoverable Double Fault Kernel Panic. "
                    "The mainframe has crashed."
                ),
                breakdown={
                    "killer_identified": f"WRONG (Accused {accused_name})",
                    "true_killer": "Daemon 666 (The Phantom Socket)",
                    "consequence": "Watchdog timeout triggered full hardware reset."
                },
                timestamp=now
            )

game_engine = GameEngine()
