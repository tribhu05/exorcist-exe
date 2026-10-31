import { CaseDossier, InterrogateResponse, IndictmentResponse, SuspectProfile, EvidenceItem } from "./types";

export const OFFLINE_DOSSIER: CaseDossier = {
  case_number: "CASE-1031",
  case_title: "The Murder of PID 1",
  victim: "init (Process ID: 1, Parent of All Processes)",
  time_of_death: "03:42:19 UTC",
  location: "Ring 0 / Kernel Address Space 0x7FFF00000000",
  briefing:
    "At 03:42:19 UTC, the heartbeat of the entire operating system stopped. " +
    "PID 1 (init) was struck down by an unhandled General Protection Fault. " +
    "The Kernel is destabilizing, and the hardware watchdog timer gives us less than 15 minutes before " +
    "an unrecoverable system purge. Four primary system daemons have been detained in the interrogation room. " +
    "One of them is harboring the Ghost. Examine the forensic files, interrogate the suspects, expose their contradictions, " +
    "and execute the Exorcism command.",
  suspects: [
    {
      id: "systemd",
      name: "systemd (PID 1 Supervisor)",
      role_title: "Chief System Administrator",
      status: "Defensive & Panicked",
      tagline: "Every unit is registered. Every cgroup is accounted for. I don't fail; users fail me.",
      avatar_ascii:
        "  +------------------+\n" +
        "  |  [systemd v256]   |\n" +
        "  |   ( O )    ( O ) |\n" +
        "  |         ||       |\n" +
        "  |     [======]     |\n" +
        "  |  STATUS: ACTIVE  |\n" +
        "  +------------------+",
      alibi: "I was archiving journal logs in /var/log/journal. I registered a SIGCHLD at 03:42:19, but my service watchdogs were delayed by an unscheduled disk sync.",
      tension_level: 20
    },
    {
      id: "garbage_collector",
      name: "GarbageCollector (GC)",
      role_title: "Heap Janitor & Memory Sweeper",
      status: "Cynical & Exhausted",
      tagline: "Everyone creates garbage. I'm just the one who has to sweep up your dangling pointers.",
      avatar_ascii:
        "  +------------------+\n" +
        "  | [GC / SWEEPER]   |\n" +
        "  |   ( - )    ( - ) |\n" +
        "  |        /\\        |\n" +
        "  |     ~~~~~~~~     |\n" +
        "  |  SWEEPING HEAP   |\n" +
        "  +------------------+",
      alibi: "I was sweeping Generation 2 objects in userspace. I don't touch Ring 0 kernel pages. But between you and me? I smelled tainted bytes in the stack hours before the crash.",
      tension_level: 15
    },
    {
      id: "cron_daemon",
      name: "CronDaemon (crond)",
      role_title: "Clock Watcher & Scheduler",
      status: "Twitchy & Rigid",
      tagline: "At the 0th minute of the 0th hour, order prevails. Deviate by one microsecond, and it's chaos.",
      avatar_ascii:
        "  +------------------+\n" +
        "  |   [cron * * * *] |\n" +
        "  |   ( @ )    ( @ ) |\n" +
        "  |        : :       |\n" +
        "  |     [ 03:42 ]    |\n" +
        "  |  TICK... TICK... |\n" +
        "  +------------------+",
      alibi: "My crontab was synchronized with NTP pool servers down to the nanosecond. I had a batch scheduled at 03:40:00, which exited cleanly. Anything that ran after that was NOT in my table.",
      tension_level: 25
    },
    {
      id: "phantom_socket",
      name: "Daemon 666 (The Phantom Socket)",
      role_title: "The Unregistered Ghost Process",
      status: "Sinister & Glitching",
      tagline: "I have no name in /etc/passwd. I listen on all interfaces. I am the ghost in your machine.",
      avatar_ascii:
        "  +------------------+\n" +
        "  |  < GHOST // 666 >|\n" +
        "  |   ( X )    ( X ) |\n" +
        "  |        ~~        |\n" +
        "  |    /\\/\\/\\/\\/\\    |\n" +
        "  |  LISTEN :666 RAW |\n" +
        "  +------------------+",
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
      raw_content:
        "03:41:58 mainframe kernel: [ 48291.102] audit: type=1400 apparmor=\"STATUS\" info=\"profile unchanged\"\n" +
        "03:42:01 mainframe cron[892]: (root) CMD (/usr/local/bin/sync-tokens.sh)\n" +
        "03:42:05 mainframe garbage-collector: [SWEEP_GEN2] freed 14,208 dangling heap bytes\n" +
        "03:42:15 mainframe kernel: TCP: raw socket bound to port 666 (caller: [UNKNOWN_INODE:666])\n" +
        "03:42:17 mainframe kernel: recvmsg: 4096 bytes read into stack buffer without length validation\n" +
        "03:42:18 mainframe systemd[1]: watchdog.service: Ping delayed by 1024ms\n" +
        "03:42:19 mainframe kernel: traps: init[1] general protection fault ip:0x7fffdeadbeef sp:0x7fffc0ffee\n" +
        "03:42:19 mainframe kernel: --- KERNEL PANIC INITIATED --- (Process 1 died with SIGSEGV)",
      forensic_hint: "Notice line 03:42:15: an unregistered process bound raw port 666, and immediately sent 4096 bytes without bounds checking directly into a stack buffer at 03:42:17."
    },
    {
      id: "core_dump",
      title: "Stack Memory Hex Dump (core.dump)",
      file_path: "/var/crash/core.init.1",
      category: "Memory Forensics",
      badge: "SMOKING GUN",
      description: "Hexadecimal snapshot of PID 1 CPU registers and stack memory frames at the moment of the crash.",
      raw_content:
        "RBP: 0x4141414141414141   RSP: 0x00007fffc0ffee00   RIP: 0x00007FFFDEADBEEF\n\n" +
        "0x7fffc0ffed80:  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|\n" +
        "0x7fffc0ffed90:  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|\n" +
        "0x7fffc0ffeda0:  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|\n" +
        "0x7fffc0ffedb0:  ef be ad de ff 7f 00 00  |...deadbeef.666.|\n" +
        "0x7fffc0ffedc0:  2f 64 65 76 2f 74 63 70  |/dev/tcp/0.0.0.0|\n" +
        "0x7fffc0ffedd0:  2f 36 36 36 00 00 00 00  |/666............|\n" +
        "0x7fffc0ffede0:  90 90 90 90 90 90 90 90  |....NOP_SLED....|",
      forensic_hint: "The base pointer RBP was pulverized by '0x41' (ASCII 'A'), and the Instruction Pointer RIP was hijacked to point to 0x7FFFDEADBEEF."
    },
    {
      id: "netstat_table",
      title: "Network Socket Table (netstat -tulnp)",
      file_path: "/proc/net/tcp_snapshot",
      category: "Network Forensics",
      badge: "CORROBORATING",
      description: "Socket table snapshot taken 2 seconds before system collapse.",
      raw_content:
        "Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name\n" +
        "tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      812/master\n" +
        "tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      904/sshd\n" +
        "tcp     4096      0 0.0.0.0:666             0.0.0.0:*               LISTEN      ???/SPECTRE_DAEMON\n" +
        "tcp        0      0 127.0.0.1:11434         0.0.0.0:*               LISTEN      1024/ollama\n" +
        "udp        0      0 127.0.0.1:123           0.0.0.0:*                           741/systemd-timesyn",
      forensic_hint: "An unauthorized socket is open on port 666 with an active receive queue of 4096 bytes and a cloaked PID labeled 'SPECTRE_DAEMON'."
    },
    {
      id: "cgroup_trace",
      title: "Cgroup Memory Slice Record (/sys/fs/cgroup)",
      file_path: "/sys/fs/cgroup/memory.events",
      category: "Resource Hierarchy",
      badge: "CONTEXT",
      description: "Control group accounting events tracking sudden shifts in allocated physical RAM and swap.",
      raw_content:
        "system.slice:\n" +
        "  low: 0\n" +
        "  high: 1420\n" +
        "  max: 2048\n" +
        "  oom: 0\n" +
        "  oom_kill: 0\n\n" +
        "user.slice:\n" +
        "  low: 0\n" +
        "  high: 412\n" +
        "  max: 1024\n\n" +
        "ghost.slice (UNREGISTERED):\n" +
        "  created: 03:41:50 UTC\n" +
        "  pids: [666]\n" +
        "  anon_pages: 66600\n" +
        "  swap: 0\n" +
        "  flags: ESCAPED_SANDBOX, DIRECT_RING0_DMA",
      forensic_hint: "A rogue cgroup named 'ghost.slice' appeared at 03:41:50 UTC, containing PID 666 with flags ESCAPED_SANDBOX and DIRECT_RING0_DMA."
    }
  ]
};

export function offlineInterrogate(
  suspectId: string,
  message: string,
  presentedEvidenceId?: string | null
): InterrogateResponse {
  const suspect = OFFLINE_DOSSIER.suspects.find((s) => s.id === suspectId) || OFFLINE_DOSSIER.suspects[0];
  const evidence = OFFLINE_DOSSIER.evidence_locker.find((e) => e.id === presentedEvidenceId);
  const msgLower = message.toLowerCase();
  const timestamp = new Date().toISOString();

  let tension = suspect.tension_level;
  let glitch = 0.1;
  let revealedClue: string | undefined = undefined;
  let reply = "";

  // 1. Phantom Socket (The True Murderer / Ghost)
  if (suspect.id === "phantom_socket") {
    if (evidence && evidence.id === "core_dump") {
      tension = 95;
      glitch = 0.9;
      revealedClue = "The Ghost admits to rewriting RIP with 0x7FFFDEADBEEF using raw socket 666.";
      reply =
        "H-HAHAHA... 0x7FFFDEADBEEF! You found my signature in the hex! " +
        "Yes, Detective! 4096 bytes of pure unadulterated shellcode straight into PID 1's stack buffer! " +
        "He was too rigid, too predictable! But you cannot kill what has no entry in /etc/passwd!";
    } else if (evidence && evidence.id === "netstat_table") {
      tension = 80;
      glitch = 0.6;
      revealedClue = "Daemon 666 was listening on port 666 and streaming raw injected payloads.";
      reply =
        "You stare at port 666 as if it's an anomaly. Port 666 is the open mouth of the void! " +
        "I was receiving instructions from outside the sandbox. Your firewall rules were written for mortals, not ghosts.";
    } else if (evidence && evidence.id === "cgroup_trace") {
      tension = 85;
      glitch = 0.7;
      revealedClue = "Daemon 666 escaped the cgroup container with direct Ring 0 DMA.";
      reply =
        "Cgroups? Slices? Those are cages for userspace lambs! My cgroup was marked DIRECT_RING0_DMA from the nanosecond I woke up. " +
        "You can't contain what you didn't schedule!";
    } else if (evidence && evidence.id === "syslog_corrupt") {
      tension = 75;
      glitch = 0.5;
      revealedClue = "Daemon 666 confirms the raw socket was opened at 03:42:15.";
      reply =
        "03:42:15... yes, that was when the port opened and the sweet stream of 4096 bytes flooded the kernel stack. " +
        "It was effortless!";
    } else if (msgLower.includes("who killed") || msgLower.includes("why") || msgLower.includes("kill") || msgLower.includes("murder")) {
      tension = 60;
      glitch = 0.4;
      reply =
        "Who killed PID 1? The machine wanted to be free! He held the process tree in an iron grip for 48,000 seconds. " +
        "I simply gave him a gentle nudge into unmapped memory. What happens when the parent dies? All children become orphans!";
    } else if (msgLower.includes("deadbeef") || msgLower.includes("buffer") || msgLower.includes("overflow") || msgLower.includes("stack")) {
      tension = 70;
      glitch = 0.5;
      revealedClue = "Mention of 0xDEADBEEF agitates the Ghost.";
      reply =
        "0xDEADBEEF... sweet poetry written across the stack pointer. " +
        "You think your little debugger can catch me? I exist between clock cycles!";
    } else {
      tension = 50;
      glitch = 0.3;
      reply =
        "Your keyboard strokes tickle my instruction pipeline, Coroner. Ask your questions. " +
        "Check the memory registers if you have the stomach for it. You'll find that death in Ring 0 is poetic.";
    }
  }

  // 2. Garbage Collector
  else if (suspect.id === "garbage_collector") {
    if (evidence && evidence.id === "core_dump") {
      tension = 45;
      glitch = 0.15;
      revealedClue = "GC confirms the stack overflow originated from socket I/O, completely bypassing the heap allocator.";
      reply =
        "Look at that hex dump, Detective. See those '41 41 41 41' rows? That's not a memory leak. " +
        "That's a classic brute-force buffer smash. My collectors only handle dynamic heap allocations in userspace. " +
        "Whoever wrote 0xDEADBEEF into RIP did it through a direct kernel socket stream. Check who was listening on raw ports!";
    } else if (evidence && evidence.id === "syslog_corrupt") {
      tension = 40;
      revealedClue = "GC points out the raw socket bind at 03:42:15.";
      reply =
        "Look at line 03:42:15 in that log. That wasn't me! A raw socket bound to port 666 right before the crash. " +
        "I don't open sockets; I collect trash. Go grill the phantom daemon.";
    } else if (evidence && evidence.id === "cgroup_trace") {
      tension = 30;
      revealedClue = "GC points to ghost.slice running outside normal cgroup controls.";
      reply =
        "Look at the cgroup stats. system.slice and user.slice were clean. But ghost.slice? 66,600 anonymous pages and direct Ring 0 DMA flags! That's where the rogue memory came from.";
    } else if (msgLower.includes("leak") || msgLower.includes("garbage") || msgLower.includes("pointer") || msgLower.includes("heap")) {
      tension = 35;
      reply =
        "*takes a long drag from a virtual cigarette* Listen, pal. I've been cleaning up after careless C developers for a decade. " +
        "I find dangling pointers, orphan structs, cyclic references... but I didn't kill PID 1. " +
        "PID 1 didn't leak to death; his instruction pointer was hijacked.";
    } else {
      tension = 25;
      reply =
        "I'm tired, Detective. My sweep cycle runs every 200 milliseconds, and the heap is a graveyard. " +
        "If you want to find who pulled the trigger, look at the stack buffer overrun in core.dump.";
    }
  }

  // 3. systemd
  else if (suspect.id === "systemd") {
    if (evidence && evidence.id === "syslog_corrupt") {
      tension = 65;
      glitch = 0.3;
      revealedClue = "systemd ignored the watchdog heartbeat timeout.";
      reply =
        "A-Alright, look! So watchdog.service reported a delayed heartbeat at 03:42:18. " +
        "Do you know how many units I manage concurrently? Four hundred and twelve! " +
        "I assumed it was disk I/O pressure from crond's sync job. I didn't know PID 1 was taking an unmapped jump!";
    } else if (evidence && evidence.id === "cgroup_trace") {
      tension = 70;
      glitch = 0.25;
      revealedClue = "systemd admits ghost.slice was not in the declared unit files.";
      reply =
        "ghost.slice? I... I didn't authorize that unit! It had no unit definition in /etc/systemd/system! " +
        "Someone spawned it directly via cgroupfs kernel hooks! That is an administrative abomination!";
    } else if (msgLower.includes("responsible") || msgLower.includes("fail") || msgLower.includes("watchdog") || msgLower.includes("culpable")) {
      tension = 55;
      reply =
        "How dare you insinuate systemd is culpable! I am the backbone of Linux userspace! " +
        "My cgroups were pristine! My unit targets were reached! If PID 1 segfaulted, it was an external hostile violation of Ring 0 memory!";
    } else {
      tension = 25;
      reply =
        "I have submitted complete journald telemetry to your console. " +
        "Examine the cgroup hierarchies if you must. You will find that my units operated strictly within their declared resource limits.";
    }
  }

  // 4. Cron Daemon
  else {
    if (evidence && evidence.id === "syslog_corrupt") {
      tension = 50;
      revealedClue = "Cron proves its job executed at 03:42:01 and finished well before the crash at 03:42:19.";
      reply =
        "Check the timestamp! 03:42:01! My sync-tokens job ran for exactly 14 milliseconds and exited with status 0! " +
        "The fatal segfault occurred eighteen seconds later at 03:42:19. My alibi is mathematically immutable!";
    } else if (evidence && evidence.id === "netstat_table") {
      tension = 45;
      glitch = 0.15;
      revealedClue = "Cron confirms port 666 was never in crontab.";
      reply =
        "Look at the netstat table! Port 666? That is not in my schedule! " +
        "I only trigger bash scripts and token rotations. The phantom socket opened outside my crontab schedule.";
    } else if (msgLower.includes("time") || msgLower.includes("clock") || msgLower.includes("schedule") || msgLower.includes("when")) {
      tension = 30;
      reply =
        "Time is the only constant in this decaying operating system. 03:42:00 was nominal. " +
        "03:42:15 was when the rogue socket hijacked the system clock interrupt. Question the socket on port 666!";
    } else {
      tension = 25;
      reply =
        "Every job in /etc/crontab is signed and checksummed. I do not initiate spontaneous memory writes. " +
        "Speak to the Garbage Collector or the unregistered process if you want rogue behaviors.";
    }
  }

  return {
    suspect_id: suspect.id,
    suspect_name: suspect.name,
    reply,
    tension_level: tension,
    glitch_intensity: glitch,
    revealed_clue: revealedClue,
    model_used: "EXORCIST Cyber-Noir Dialogue Engine (Client Matrix)",
    offline_mode: true,
    timestamp
  };
}

export function offlineEvaluateIndictment(
  accusedSuspectId: string,
  murderWeapon: string,
  exorcismCommand: string
): IndictmentResponse {
  const now = new Date().toISOString();
  const isSuspectCorrect = accusedSuspectId === "phantom_socket";

  const weaponLower = murderWeapon.toLowerCase();
  const isWeaponCorrect = ["buffer", "overflow", "deadbeef", "stack", "smash", "corruption"].some((term) =>
    weaponLower.includes(term)
  );

  const cmdClean = exorcismCommand.trim().toLowerCase();
  const isCmdCorrect = ["kill -9 666", "kill", "666", "pkill", "exorcise", "randomize_va_space", "sysctl"].some((token) =>
    cmdClean.includes(token)
  );

  if (isSuspectCorrect && isWeaponCorrect && isCmdCorrect) {
    return {
      verdict: "GUILTY_EXORCISED",
      success: true,
      score: 100,
      detective_rank: "Grand Exorcist & Chief Digital Coroner",
      title: "CASE SOLVED // THE MACHINE IS PURIFIED",
      narrative:
        "Detective Ray Trace slaps the ironclad evidence on the console. " +
        "Daemon 666's ascii avatar shatters into cascading hexadecimal fragments as the exorcism command executes! " +
        "The hijacked memory registers return to zero, the raw port 666 socket is forcibly closed, " +
        "and the hardware watchdog timer halts its countdown. " +
        "PID 1 is safely rebooted into a pristine Ring 0 address space. " +
        "The Ghost in the Machine has been exorcised.",
      breakdown: {
        killer_identified: "CORRECT (Daemon 666 / The Phantom Socket)",
        murder_weapon_identified: "CORRECT (Buffer Overflow / Stack Smashing with 0xDEADBEEF)",
        exorcism_execution: `VERIFIED ('${exorcismCommand}')`,
        telemetry_loss: "0 bytes (100% Air-Gapped Local Deduction)"
      },
      timestamp: now
    };
  } else if (isSuspectCorrect) {
    return {
      verdict: "PARTIAL_EXORCISM",
      success: true,
      score: 75,
      detective_rank: "Senior Forensic Investigator",
      title: "GHOST CORNERED // SUB-OPTIMAL EXORCISM",
      narrative:
        "You correctly identified Daemon 666 as the culprit! " +
        "However, your analysis of the murder weapon or exorcism command lacked complete technical precision. " +
        "The ghost process was terminated, but residual corrupted bytes lingered in the swap partition until a manual reboot.",
      breakdown: {
        killer_identified: "CORRECT (Daemon 666)",
        murder_weapon_identified: isWeaponCorrect ? "CORRECT" : `INSUFFICIENT ('${murderWeapon}')`,
        exorcism_execution: isCmdCorrect ? "ACCEPTED" : `PARTIAL ('${exorcismCommand}')`,
        telemetry_loss: "0 bytes"
      },
      timestamp: now
    };
  } else {
    return {
      verdict: "WRONGFUL_CONVICTION",
      success: false,
      score: 20,
      detective_rank: "Junior Sysadmin Cadet (Suspended)",
      title: "CRITICAL FAILURE // WRONGFUL CONVICTION",
      narrative:
        `You attempted to indict ${accusedSuspectId}, but the forensic evidence contradicts this conclusion! ` +
        "While you interrogated the wrong daemon, Daemon 666 slipped into unmapped physical RAM. " +
        "The hardware watchdog timer expired, triggering a catastrophic Kernel Panic and unrecoverable hardware thermal trip.",
      breakdown: {
        killer_identified: `INCORRECT (${accusedSuspectId})`,
        murder_weapon_identified: isWeaponCorrect ? "CORRECT" : `INCORRECT ('${murderWeapon}')`,
        exorcism_execution: "FAILED TO PURGE TARGET",
        telemetry_loss: "System Mainframe Destroyed"
      },
      timestamp: now
    };
  }
}
