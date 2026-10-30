import asyncio
import time
import os
from typing import Tuple

BLOCKED_PATTERNS = [
    ":(){ :|:& };:", # forkbomb
    "rm -rf /",
    "rm -rf /*",
    "mkfs",
    "dd if=/dev/zero",
    "> /dev/sda"
]

class ShellRunner:
    async def execute(
        self,
        command: str,
        cwd: str = None,
        timeout: int = 15
    ) -> Tuple[int, str, str, float]:
        """
        Executes a shell command safely, capturing exit code, stdout, stderr and duration.
        """
        start_time = time.perf_counter()

        # Security check
        for pattern in BLOCKED_PATTERNS:
            if pattern in command:
                duration_ms = (time.perf_counter() - start_time) * 1000
                return 1, "", f"SECURITY FAULT: Command blocked by PHANTOM safety barrier (Forbidden pattern: {pattern})", duration_ms

        working_dir = cwd if cwd and os.path.isdir(cwd) else None

        try:
            # On Windows use cmd.exe /c or powershell
            is_windows = os.name == "nt"
            if is_windows:
                cmd_args = ["cmd.exe", "/c", command]
            else:
                cmd_args = ["/bin/sh", "-c", command]

            process = await asyncio.create_subprocess_exec(
                *cmd_args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir
            )

            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(process.communicate(), timeout=timeout)
                exit_code = process.returncode if process.returncode is not None else 0
                stdout = stdout_bytes.decode("utf-8", errors="replace")
                stderr = stderr_bytes.decode("utf-8", errors="replace")
            except asyncio.TimeoutError:
                try:
                    process.kill()
                except Exception:
                    pass
                exit_code = 124
                stdout = ""
                stderr = f"TIMEOUT: Execution timed out after {timeout} seconds."

        except Exception as e:
            exit_code = 1
            stdout = ""
            stderr = f"EXECUTION ERROR: {str(e)}"

        duration_ms = (time.perf_counter() - start_time) * 1000
        return exit_code, stdout, stderr, duration_ms

shell_runner = ShellRunner()
