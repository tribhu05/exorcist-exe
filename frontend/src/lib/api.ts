import { CaseDossier, InterrogateResponse, IndictmentResponse, SystemStatus } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchCaseDossier(): Promise<CaseDossier> {
  try {
    const res = await fetch(`${API_BASE}/api/game/case`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch case dossier");
    return await res.json();
  } catch (err) {
    console.warn("Using offline bundled dossier:", err);
    // Offline bundled fallback
    return {
      case_number: "CASE-1031",
      case_title: "The Murder of PID 1",
      victim: "init (Process ID: 1, Parent of All Processes)",
      time_of_death: "03:42:19 UTC",
      location: "Ring 0 / Kernel Address Space 0x7FFF00000000",
      briefing: "At 03:42:19 UTC, the heartbeat of the entire operating system stopped. PID 1 was struck down by an unhandled General Protection Fault. Interrogate the 4 detained system daemons, examine the evidence, and execute the Exorcism before watchdog triggers a full Kernel Panic.",
      suspects: [
        {
          id: "systemd",
          name: "systemd (PID 1 Supervisor)",
          role_title: "Chief System Administrator",
          status: "Defensive & Panicked",
          tagline: "Every unit is registered. Every cgroup is accounted for. I don't fail; users fail me.",
          avatar_ascii: "  [systemd v256]\n   ( O )    ( O )\n         ||\n     [======]\n  STATUS: ACTIVE",
          alibi: "I was archiving journal logs in /var/log/journal. I registered a SIGCHLD at 03:42:19, but my service watchdogs were delayed by an unscheduled disk sync.",
          tension_level: 20
        },
        {
          id: "garbage_collector",
          name: "GarbageCollector (GC)",
          role_title: "Heap Janitor & Memory Sweeper",
          status: "Cynical & Exhausted",
          tagline: "Everyone creates garbage. I'm just the one who has to sweep up your dangling pointers.",
          avatar_ascii: " [GC / SWEEPER]\n   ( - )    ( - )\n        /\\\n     ~~~~~~~~\n  SWEEPING HEAP",
          alibi: "I was sweeping Generation 2 objects in userspace. I don't touch Ring 0 kernel pages. But between you and me? I smelled tainted bytes in the stack hours before the crash.",
          tension_level: 15
        },
        {
          id: "cron_daemon",
          name: "CronDaemon (crond)",
          role_title: "Clock Watcher & Scheduler",
          status: "Twitchy & Rigid",
          tagline: "At the 0th minute of the 0th hour, order prevails. Deviate by one microsecond, and it's chaos.",
          avatar_ascii: "   [cron * * * *]\n   ( @ )    ( @ )\n        : :\n     [ 03:42 ]\n  TICK... TICK...",
          alibi: "My crontab was synchronized with NTP pool servers down to the nanosecond. I had a batch scheduled at 03:40:00, which exited cleanly. Anything that ran after that was NOT in my table.",
          tension_level: 25
        },
        {
          id: "phantom_socket",
          name: "Daemon 666 (The Phantom Socket)",
          role_title: "The Unregistered Ghost Process",
          status: "Sinister & Glitching",
          tagline: "I have no name in /etc/passwd. I listen on all interfaces. I am the ghost in your machine.",
          avatar_ascii: "  < GHOST // 666 >\n   ( X )    ( X )\n        ~~\n    /\\/\\/\\/\\/\\\n  LISTEN :666 RAW",
          alibi: "Alibi? You mortal detectives measure time in CPU cycles. I have lived inside the machine's silicon since bootloader stage 1. PID 1 didn't die... he was simply rewritten.",
          tension_level: 40
        }
      ],
      evidence_locker: [
        {
          id: "syslog_corrupt",
          title: "Corrupted Syslog (/var/log/syslog)",
          file_path: "/var/log/syslog",
          category: "System Logs",
          badge: "TIMELINE CRUCIAL",
          description: "Chronological log entries captured by syslogd leading up to the exact millisecond of PID 1's demise.",
          raw_content: "03:42:15 mainframe kernel: TCP: raw socket bound to port 666 (caller: [UNKNOWN_INODE:666])\n03:42:17 mainframe kernel: recvmsg: 4096 bytes read into stack buffer without length validation\n03:42:19 mainframe kernel: traps: init[1] general protection fault ip:0x7fffdeadbeef sp:0x7fffc0ffee\n03:42:19 mainframe kernel: --- KERNEL PANIC INITIATED --- (Process 1 died with SIGSEGV)",
          forensic_hint: "Notice line 03:42:15: an unregistered process bound raw port 666, and immediately sent 4096 bytes without bounds checking directly into a stack buffer at 03:42:17."
        },
        {
          id: "core_dump",
          title: "Stack Memory Hex Dump (core.dump)",
          file_path: "/var/crash/core.init.1",
          category: "Memory Forensics",
          badge: "SMOKING GUN",
          description: "Hexadecimal snapshot of PID 1 CPU registers and stack memory frames at the moment of the crash.",
          raw_content: "RBP: 0x4141414141414141   RSP: 0x00007fffc0ffee00   RIP: 0x00007FFFDEADBEEF\n\n0x7fffc0ffed80:  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|\n0x7fffc0ffedb0:  ef be ad de ff 7f 00 00  |...deadbeef.666.|\n0x7fffc0ffedc0:  2f 64 65 76 2f 74 63 70  |/dev/tcp/0.0.0.0|",
          forensic_hint: "The base pointer RBP was pulverized by '0x41' (ASCII 'A'), and the Instruction Pointer RIP was hijacked to point to 0x7FFFDEADBEEF."
        },
        {
          id: "netstat_table",
          title: "Network Socket Table (netstat -tulnp)",
          file_path: "/proc/net/tcp_snapshot",
          category: "Network Forensics",
          badge: "CORROBORATING",
          description: "Socket table snapshot taken 2 seconds before system collapse.",
          raw_content: "tcp     4096      0 0.0.0.0:666             0.0.0.0:*               LISTEN      ???/SPECTRE_DAEMON",
          forensic_hint: "An unauthorized socket is open on port 666 with an active receive queue of 4096 bytes."
        },
        {
          id: "cgroup_trace",
          title: "Cgroup Memory Slice Record (/sys/fs/cgroup)",
          file_path: "/sys/fs/cgroup/memory.events",
          category: "Resource Hierarchy",
          badge: "CONTEXT",
          description: "Control group accounting events tracking sudden shifts in allocated physical RAM and swap.",
          raw_content: "ghost.slice (UNREGISTERED):\n  created: 03:41:50 UTC\n  pids: [666]\n  flags: ESCAPED_SANDBOX, DIRECT_RING0_DMA",
          forensic_hint: "A rogue cgroup named 'ghost.slice' appeared at 03:41:50 UTC, containing PID 666 with flags ESCAPED_SANDBOX."
        }
      ]
    };
  }
}

export async function sendInterrogation(
  suspectId: string,
  message: string,
  presentedEvidenceId?: string
): Promise<InterrogateResponse> {
  try {
    const res = await fetch(`${API_BASE}/api/game/interrogate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        suspect_id: suspectId,
        message,
        presented_evidence_id: presentedEvidenceId || null,
      }),
    });
    if (!res.ok) throw new Error("Interrogation request failed");
    return await res.json();
  } catch (err) {
    console.warn("Falling back to local client reply:", err);
    return {
      suspect_id: suspectId,
      suspect_name: suspectId,
      reply: "The daemon shifts restlessly in its allocated cgroup. 'You can inspect my registers all you want, Detective. The Ghost is elsewhere.'",
      tension_level: 50,
      glitch_intensity: 0.2,
      model_used: "Offline Client Matrix",
      offline_mode: true,
      timestamp: new Date().toISOString()
    };
  }
}

export async function submitIndictment(
  accusedSuspectId: string,
  murderWeapon: string,
  exorcismCommand: string
): Promise<IndictmentResponse> {
  const res = await fetch(`${API_BASE}/api/game/indict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      accused_suspect_id: accusedSuspectId,
      murder_weapon: murderWeapon,
      exorcism_command: exorcismCommand,
    }),
  });
  if (!res.ok) throw new Error("Indictment request failed");
  return await res.json();
}

export async function fetchSystemStatus(): Promise<SystemStatus> {
  try {
    const res = await fetch(`${API_BASE}/api/status`, { cache: "no-store" });
    if (!res.ok) throw new Error("Status failed");
    return await res.json();
  } catch {
    return {
      app_name: "EXORCIST.EXE // PHANTOM",
      version: "1.0.0",
      tagline: "The Ghost in your Terminal. Local. Offline. Omnipresent.",
      model_configured: "gemma2:2b",
      ollama_endpoint: "http://localhost:11434",
      ollama_reachable: false,
      offline_fallback_active: true,
      total_incidents_recorded: 4,
      airgap_verified: true
    };
  }
}
