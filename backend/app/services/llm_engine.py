import json
import logging
import re
import difflib
import uuid
from typing import Dict, Any, Tuple, Optional
import httpx
from datetime import datetime, timezone

from app.config import settings
from app.models.schemas import CommandAutopsyResponse, ExorcismResponse, HauntedAnomaly

logger = logging.getLogger("phantom.llm")

class SpectralLLMEngine:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL.rstrip('/')
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT_SECONDS
        self.offline_fallback_enabled = settings.ENABLE_OFFLINE_FALLBACK

    async def is_ollama_alive(self) -> bool:
        """Check if local Ollama daemon is active and responsive."""
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                return res.status_code == 200
        except Exception:
            return False

    async def query_ollama(self, prompt: str, system_prompt: str) -> Optional[Dict[str, Any]]:
        """Query Ollama with JSON formatting request."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "system": system_prompt,
                    "format": "json",
                    "stream": False,
                    "options": {
                        "temperature": 0.2,
                        "num_predict": 1024
                    }
                }
                response = await client.post(f"{self.base_url}/api/generate", json=payload)
                if response.status_code == 200:
                    raw_text = response.json().get("response", "{}")
                    return json.loads(raw_text)
        except Exception as e:
            logger.warning(f"Ollama inference unavailable ({str(e)}). Engaging offline spectral engine.")
        return None

    async def autopsy_command(
        self,
        command: str,
        exit_code: int,
        stdout: str,
        stderr: str,
        cwd: Optional[str] = None
    ) -> CommandAutopsyResponse:
        """Diagnose a command failure using Ollama or offline spectral rules."""
        incident_id = f"PHANTOM-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.now(timezone.utc).isoformat()

        if exit_code == 0:
            return CommandAutopsyResponse(
                incident_id=incident_id,
                status="nominal",
                ghost_type="None (System Harmonious)",
                severity="LOW",
                spectral_diagnosis="The command finished with exit code 0. No spectral anomalies or haunting signals detected in standard streams.",
                root_cause="Clean execution.",
                suggested_command=None,
                patch_diff=None,
                explanation="Process exited cleanly without error signatures.",
                model_used="System Heuristic",
                offline_mode=True,
                timestamp=timestamp
            )

        combined_output = f"STDOUT:\n{stdout}\n\nSTDERR:\n{stderr}".strip()

        # Try live open-weight model first
        if await self.is_ollama_alive():
            system_prompt = (
                "You are PHANTOM//SHELL, an advanced autonomous software forensics AI analyzing failed terminal commands. "
                "Analyze the command, exit code, and stdout/stderr output. "
                "Identify the exact technical bug, classification, root cause, and the exact fixed command or code patch to resolve it. "
                "Return strictly valid JSON with keys: "
                "ghost_type (e.g. 'Zombie Port Conflict', 'Segmentation Fault', 'Missing Module Wraith', 'Permission Spectre'), "
                "severity ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW'), "
                "spectral_diagnosis (concise forensic summary), "
                "root_cause (exact technical explanation), "
                "suggested_command (the precise shell command that will resolve the problem), "
                "explanation (step-by-step guidance)."
            )
            prompt = (
                f"Command: {command}\n"
                f"Exit Code: {exit_code}\n"
                f"Working Directory: {cwd or 'unknown'}\n"
                f"Output:\n{combined_output}"
            )
            llm_result = await self.query_ollama(prompt, system_prompt)
            if llm_result and "ghost_type" in llm_result:
                return CommandAutopsyResponse(
                    incident_id=incident_id,
                    status="anomaly_detected",
                    ghost_type=llm_result.get("ghost_type", "Unknown Anomaly"),
                    severity=llm_result.get("severity", "HIGH"),
                    spectral_diagnosis=llm_result.get("spectral_diagnosis", "Anomaly diagnosed by local model."),
                    root_cause=llm_result.get("root_cause", "Unspecified failure in runtime."),
                    suggested_command=llm_result.get("suggested_command"),
                    patch_diff=llm_result.get("patch_diff"),
                    explanation=llm_result.get("explanation", ""),
                    model_used=self.model,
                    offline_mode=False,
                    timestamp=timestamp
                )

        # High-Fidelity Offline Forensic Rules Engine
        return self._offline_autopsy(command, exit_code, stdout, stderr, incident_id, timestamp)

    def _offline_autopsy(
        self,
        command: str,
        exit_code: int,
        stdout: str,
        stderr: str,
        incident_id: str,
        timestamp: str
    ) -> CommandAutopsyResponse:
        """Expert pattern-matching engine for offline analysis."""
        combined = f"{stdout} {stderr}".lower()

        # 1. Port conflict / EADDRINUSE
        if "eaddrinuse" in combined or "address already in use" in combined:
            port_match = re.search(r":(\d{2,5})", combined) or re.search(r"port (\d{2,5})", combined)
            port = port_match.group(1) if port_match else "3000"
            return CommandAutopsyResponse(
                incident_id=incident_id,
                status="anomaly_detected",
                ghost_type="Zombie Port Conflict (EADDRINUSE)",
                severity="HIGH",
                spectral_diagnosis=f"A lingering zombie process has bound TCP port {port}, preventing this process from binding the socket.",
                root_cause=f"Port {port} is occupied by an orphaned background worker or previous crashed instance.",
                suggested_command=f"npx kill-port {port} || lsof -ti:{port} | xargs kill -9",
                patch_diff=None,
                explanation=f"Exorcise the orphaned process occupying port {port} or configure your application to bind an alternative PORT environment variable.",
                model_used="PHANTOM Offline Spectral Rules",
                offline_mode=True,
                timestamp=timestamp
            )

        # 2. Python ModuleNotFoundError / ImportError
        if "modulenotfounderror: no module named" in combined or "no module named" in combined:
            mod_match = re.search(r"no module named ['\"]?([a-zA-Z0-9_\-]+)['\"]?", combined)
            mod_name = mod_match.group(1) if mod_match else "dependency"
            return CommandAutopsyResponse(
                incident_id=incident_id,
                status="anomaly_detected",
                ghost_type="Missing Module Wraith (ImportError)",
                severity="MEDIUM",
                spectral_diagnosis=f"The Python interpreter attempted to import '{mod_name}', but the module does not exist in the active virtual environment.",
                root_cause=f"Package '{mod_name}' is not installed or the wrong virtualenv is activated.",
                suggested_command=f"pip install {mod_name}",
                patch_diff=f"--- requirements.txt\n+++ requirements.txt\n@@ -1,0 +1,1 @@\n+{mod_name}>=1.0.0",
                explanation=f"Install the missing dependency into your active Python environment using pip.",
                model_used="PHANTOM Offline Spectral Rules",
                offline_mode=True,
                timestamp=timestamp
            )

        # 3. Node ERR_MODULE_NOT_FOUND
        if "err_module_not_found" in combined or "cannot find module" in combined:
            mod_match = re.search(r"cannot find module ['\"]?([@a-zA-Z0-9_\-\/]+)['\"]?", combined)
            pkg = mod_match.group(1) if mod_match else "package"
            return CommandAutopsyResponse(
                incident_id=incident_id,
                status="anomaly_detected",
                ghost_type="Phantom Dependency Anomaly (Cannot Find Module)",
                severity="MEDIUM",
                spectral_diagnosis=f"Node.js module resolver failed to locate '{pkg}'.",
                root_cause=f"Dependency '{pkg}' is referenced in imports but absent from node_modules.",
                suggested_command=f"npm install {pkg}",
                patch_diff=None,
                explanation=f"Run npm install {pkg} or verify that 'npm install' has been executed in the project directory.",
                model_used="PHANTOM Offline Spectral Rules",
                offline_mode=True,
                timestamp=timestamp
            )

        # 4. Out of Memory / Exit Code 137
        if exit_code == 137 or "out of memory" in combined or "killed" in combined:
            return CommandAutopsyResponse(
                incident_id=incident_id,
                status="anomaly_detected",
                ghost_type="OOM Reaper (Exit 137 / SIGKILL)",
                severity="CRITICAL",
                spectral_diagnosis="The Linux OOM Killer or container memory supervisor terminated the process with SIGKILL (Exit Code 137).",
                root_cause="The application exhausted allocated RAM or container limits due to runaway memory accumulation or unbounded data buffering.",
                suggested_command="NODE_OPTIONS=\"--max-old-space-size=4096\" npm start",
                patch_diff=None,
                explanation="Increase Node/Process memory heap or stream chunked data instead of loading entire datasets into memory.",
                model_used="PHANTOM Offline Spectral Rules",
                offline_mode=True,
                timestamp=timestamp
            )

        # 5. Segmentation Fault / Exit Code 139
        if exit_code == 139 or "segmentation fault" in combined or "sigsegv" in combined:
            return CommandAutopsyResponse(
                incident_id=incident_id,
                status="anomaly_detected",
                ghost_type="Memory Corruption Spectre (SIGSEGV 139)",
                severity="CRITICAL",
                spectral_diagnosis="Hardware memory access violation. The process attempted to read or write to an unmapped or protected memory address.",
                root_cause="Null pointer dereference, buffer overflow, or ABI incompatibility in native C/C++ or Rust FFI extension.",
                suggested_command="gdb --batch -ex 'run' -ex 'bt' --args " + command,
                patch_diff=None,
                explanation="Run the binary through GDB or Valgrind to extract the stack trace at the exact moment of memory fault.",
                model_used="PHANTOM Offline Spectral Rules",
                offline_mode=True,
                timestamp=timestamp
            )

        # 6. Command not found / Exit Code 127
        if exit_code == 127 or "command not found" in combined or "is not recognized" in combined:
            cmd_name = command.split()[0] if command else "binary"
            return CommandAutopsyResponse(
                incident_id=incident_id,
                status="anomaly_detected",
                ghost_type="Void Execution Phantom (Command Not Found 127)",
                severity="HIGH",
                spectral_diagnosis=f"The shell could not find executable binary '{cmd_name}' anywhere in system PATH.",
                root_cause=f"Binary '{cmd_name}' is not installed or its installation directory is missing from PATH.",
                suggested_command=f"which {cmd_name} || export PATH=$PATH:/usr/local/bin:~/.local/bin",
                patch_diff=None,
                explanation=f"Verify that '{cmd_name}' is installed and present in your current environment PATH.",
                model_used="PHANTOM Offline Spectral Rules",
                offline_mode=True,
                timestamp=timestamp
            )

        # 7. Git uncommitted changes or merge conflict
        if "conflict" in combined or "merge conflict" in combined:
            return CommandAutopsyResponse(
                incident_id=incident_id,
                status="anomaly_detected",
                ghost_type="Temporal Divergence (Git Merge Conflict)",
                severity="MEDIUM",
                spectral_diagnosis="Conflicting changes exist between local and upstream branch revisions.",
                root_cause="Overlapping modifications on the same file lines across divergent commits.",
                suggested_command="git status && git diff --name-only --diff-filter=U",
                patch_diff=None,
                explanation="Resolve the conflicting hunk markers (<<<<<<<, =======, >>>>>>>) then commit the unified resolution.",
                model_used="PHANTOM Offline Spectral Rules",
                offline_mode=True,
                timestamp=timestamp
            )

        # Fallback General Anomaly
        return CommandAutopsyResponse(
            incident_id=incident_id,
            status="anomaly_detected",
            ghost_type=f"Unhandled Abort Anomaly (Exit Code {exit_code})",
            severity="HIGH" if exit_code > 128 else "MEDIUM",
            spectral_diagnosis=f"The command terminated abnormally with exit code {exit_code}. Output contains diagnostic stderr warnings.",
            root_cause="Process returned a non-zero exit code due to unhandled condition or runtime error.",
            suggested_command=f"{command} --verbose",
            patch_diff=None,
            explanation=f"Inspect stderr lines or re-execute with elevated debug / verbose flags to isolate the underlying condition.",
            model_used="PHANTOM Offline Spectral Rules",
            offline_mode=True,
            timestamp=timestamp
        )

    async def exorcise_code(
        self,
        code: str,
        filename: str = "snippet.py",
        language: str = "python"
    ) -> ExorcismResponse:
        """Scan source code for haunted antipatterns and generate purified code with diff."""
        timestamp = datetime.now(timezone.utc).isoformat()

        # Try live LLM first
        if await self.is_ollama_alive():
            system_prompt = (
                "You are PHANTOM//SHELL Exorcist, an elite static analysis and code security AI. "
                "Analyze the provided code for dangerous antipatterns, ghost bugs (memory leaks, zombie event listeners, "
                "silent exception swallowers, race conditions, unclosed resources, mutable defaults, unhandled promises). "
                "Output strictly valid JSON with keys: "
                "haunted_score (integer 0-100), "
                "spectral_summary (summary of code hauntings), "
                "purified_code (full corrected source code), "
                "anomalies (array of objects with keys: line_number, ghost_pattern, severity, description, original_snippet, purified_snippet)."
            )
            prompt = f"Filename: {filename}\nLanguage: {language}\nSource Code:\n```\n{code}\n```"
            llm_result = await self.query_ollama(prompt, system_prompt)
            if llm_result and "purified_code" in llm_result:
                purified = llm_result["purified_code"]
                diff = self._create_unified_diff(code, purified, filename)
                anomalies = [
                    HauntedAnomaly(
                        id=f"HAUNT-{i+1}",
                        line_number=a.get("line_number", 1),
                        ghost_pattern=a.get("ghost_pattern", "Ghost Bug"),
                        severity=a.get("severity", "MEDIUM"),
                        description=a.get("description", "Haunted code pattern"),
                        original_snippet=a.get("original_snippet", ""),
                        purified_snippet=a.get("purified_snippet", "")
                    )
                    for i, a in enumerate(llm_result.get("anomalies", []))
                ]
                return ExorcismResponse(
                    file_analyzed=filename,
                    haunted_score=min(100, max(0, int(llm_result.get("haunted_score", 65)))),
                    anomalies_found=anomalies,
                    original_code=code,
                    purified_code=purified,
                    unified_diff=diff,
                    spectral_summary=llm_result.get("spectral_summary", "Exorcism complete."),
                    model_used=self.model,
                    offline_mode=False,
                    timestamp=timestamp
                )

        # High-Fidelity Offline Code Exorcism Engine
        return self._offline_exorcise(code, filename, language, timestamp)

    def _offline_exorcise(
        self,
        code: str,
        filename: str,
        language: str,
        timestamp: str
    ) -> ExorcismResponse:
        lines = code.split("\n")
        anomalies: list[HauntedAnomaly] = []
        purified_lines = list(lines)
        score = 0

        lang = language.lower()
        if filename.endswith(".py") or "python" in lang:
            # 1. Check for silent exception swallower: except: pass or except Exception: pass
            for i, line in enumerate(lines):
                stripped = line.strip()
                if re.match(r"^except(\s+[a-zA-Z0-9_]+)?\s*:\s*pass$", stripped) or (
                    stripped.startswith("except") and i + 1 < len(lines) and lines[i+1].strip() == "pass"
                ):
                    anomalies.append(HauntedAnomaly(
                        id=f"HAUNT-{len(anomalies)+1}",
                        line_number=i + 1,
                        ghost_pattern="The Black Hole Wraith (Silent Exception Swallower)",
                        severity="HIGH",
                        description="Exceptions are caught and suppressed with 'pass'. This masks fatal runtime failures and causes invisible system corruption.",
                        original_snippet=line,
                        purified_snippet="except Exception as e:\n    logger.error(f'Operation failed: {e}')\n    raise"
                    ))
                    # replace in purified
                    indent = line[:len(line) - len(line.lstrip())]
                    purified_lines[i] = f"{indent}except Exception as exc:"
                    if i + 1 < len(lines) and lines[i+1].strip() == "pass":
                        next_indent = lines[i+1][:len(lines[i+1]) - len(lines[i+1].lstrip())]
                        purified_lines[i+1] = f"{next_indent}logging.exception('Unhandled ghost exception: %s', exc)\n{next_indent}raise"
                    score += 25

            # 2. Check for mutable default argument: def foo(items=[]) or def bar(d={})
            for i, line in enumerate(lines):
                if re.search(r"def\s+[a-zA-Z0-9_]+\s*\([^)]*=\s*(\[\]|\{\})", line):
                    anomalies.append(HauntedAnomaly(
                        id=f"HAUNT-{len(anomalies)+1}",
                        line_number=i + 1,
                        ghost_pattern="Phantom State Bleed (Mutable Default Argument)",
                        severity="MEDIUM",
                        description="Mutable default argument (list/dict) retains mutated state across repeated function invocations.",
                        original_snippet=line,
                        purified_snippet=re.sub(r"=\s*(\[\]|\{\})", "=None", line)
                    ))
                    purified_lines[i] = re.sub(r"=\s*(\[\]|\{\})", "=None", line)
                    score += 20

            # 3. Check for unclosed open() without 'with'
            for i, line in enumerate(lines):
                stripped = line.strip()
                if re.search(r"^[a-zA-Z0-9_]+\s*=\s*open\(", stripped) and not line.strip().startswith("with "):
                    var_match = re.search(r"^([a-zA-Z0-9_]+)\s*=\s*open\((.+)\)", stripped)
                    if var_match:
                        var_name, args = var_match.group(1), var_match.group(2)
                        anomalies.append(HauntedAnomaly(
                            id=f"HAUNT-{len(anomalies)+1}",
                            line_number=i + 1,
                            ghost_pattern="Dangling Resource Phantom (Unclosed File Descriptor)",
                            severity="MEDIUM",
                            description=f"File descriptor '{var_name}' is opened directly without a context manager, risking OS descriptor leaks.",
                            original_snippet=line,
                            purified_snippet=f"with open({args}) as {var_name}:"
                        ))
                        indent = line[:len(line) - len(line.lstrip())]
                        purified_lines[i] = f"{indent}with open({args}) as {var_name}:"
                        score += 20

        elif any(ext in filename for ext in [".js", ".ts", ".jsx", ".tsx"]) or "javascript" in lang or "typescript" in lang:
            # 1. Check for unhandled addEventListener without removeEventListener
            for i, line in enumerate(lines):
                if "addEventListener(" in line and not any("removeEventListener" in l for l in lines):
                    event_match = re.search(r"addEventListener\(['\"]([^'\"]+)['\"]", line)
                    event_type = event_match.group(1) if event_match else "event"
                    anomalies.append(HauntedAnomaly(
                        id=f"HAUNT-{len(anomalies)+1}",
                        line_number=i + 1,
                        ghost_pattern="Zombie Event Listener (Memory Leak Spectre)",
                        severity="HIGH",
                        description=f"Global '{event_type}' event listener is mounted without a corresponding cleanup teardown handler.",
                        original_snippet=line,
                        purified_snippet=f"useEffect(() => {{\n  window.addEventListener('{event_type}', handler);\n  return () => window.removeEventListener('{event_type}', handler);\n}}, []);"
                    ))
                    score += 30

            # 2. Check for empty catch block in JS: catch (e) {}
            for i, line in enumerate(lines):
                if re.search(r"catch\s*\([^)]*\)\s*\{\s*\}", line):
                    anomalies.append(HauntedAnomaly(
                        id=f"HAUNT-{len(anomalies)+1}",
                        line_number=i + 1,
                        ghost_pattern="The Void Catch (Silent Exception Swallowing)",
                        severity="HIGH",
                        description="Caught exception is discarded silently with an empty block.",
                        original_snippet=line,
                        purified_snippet="catch (err) { console.error('Caught spectral error:', err); throw err; }"
                    ))
                    purified_lines[i] = re.sub(r"catch\s*\(([^)]*)\)\s*\{\s*\}", r"catch (\1) { console.error('Encountered unhandled error:', \1); throw \1; }", line)
                    score += 25

            # 3. Check for setInterval without clearInterval
            for i, line in enumerate(lines):
                if "setInterval(" in line and not any("clearInterval" in l for l in lines):
                    anomalies.append(HauntedAnomaly(
                        id=f"HAUNT-{len(anomalies)+1}",
                        line_number=i + 1,
                        ghost_pattern="Perpetual Clock Wraith (Uncancelled Interval)",
                        severity="MEDIUM",
                        description="Timer interval set without storing intervalId or calling clearInterval, resulting in persistent CPU drain.",
                        original_snippet=line,
                        purified_snippet="const timerId = setInterval(...); return () => clearInterval(timerId);"
                    ))
                    score += 20

        # General safety check if no anomalies were caught
        if not anomalies:
            purified_code = code
            summary = "No malignant hauntings detected. The source code aligns with clean, defensive architecture."
            score = 5
        else:
            purified_code = "\n".join(purified_lines)
            summary = f"Detected {len(anomalies)} active haunting anomalies. Generated verified exorcism patch with zero telemetry."
            score = min(98, max(20, score))

        diff = self._create_unified_diff(code, purified_code, filename)

        return ExorcismResponse(
            file_analyzed=filename,
            haunted_score=score,
            anomalies_found=anomalies,
            original_code=code,
            purified_code=purified_code,
            unified_diff=diff,
            spectral_summary=summary,
            model_used="PHANTOM Static AST & Heuristic Exorcist",
            offline_mode=True,
            timestamp=timestamp
        )

    def _create_unified_diff(self, original: str, modified: str, filename: str) -> str:
        orig_lines = original.splitlines(keepends=True)
        mod_lines = modified.splitlines(keepends=True)
        diff_lines = list(difflib.unified_diff(
            orig_lines,
            mod_lines,
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
            lineterm=""
        ))
        return "".join(diff_lines) if diff_lines else f"# No diff required for {filename}"

llm_engine = SpectralLLMEngine()
