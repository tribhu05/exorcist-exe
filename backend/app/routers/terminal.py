from fastapi import APIRouter
from app.models.schemas import ExecuteCommandRequest, ExecuteCommandResponse
from app.services.shell_runner import shell_runner
from app.services.llm_engine import llm_engine
from app.services.grimoire_store import grimoire_store

router = APIRouter(prefix="/api/terminal", tags=["Terminal"])

@router.post("/execute", response_model=ExecuteCommandResponse)
async def execute_command(req: ExecuteCommandRequest):
    exit_code, stdout, stderr, duration_ms = await shell_runner.execute(
        command=req.command,
        cwd=req.cwd,
        timeout=req.timeout or 15
    )

    autopsy = None
    if exit_code != 0:
        autopsy = await llm_engine.autopsy_command(
            command=req.command,
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            cwd=req.cwd
        )
        if autopsy.status == "anomaly_detected":
            grimoire_store.record_incident(
                incident_id=autopsy.incident_id,
                incident_type="COMMAND_AUTOPSY",
                title=f"{autopsy.ghost_type} ({req.command})",
                severity=autopsy.severity,
                details=autopsy.model_dump()
            )

    return ExecuteCommandResponse(
        command=req.command,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
        duration_ms=round(duration_ms, 2),
        autopsy=autopsy
    )

@router.get("/presets")
async def get_anomaly_presets():
    """Return pre-configured realistic anomaly scenarios for instant demonstration."""
    return [
        {
            "id": "port-conflict",
            "name": "Zombie Port Conflict (EADDRINUSE)",
            "command": "node -e 'require(\"net\").createServer().listen(3000, () => { throw new Error(\"listen EADDRINUSE: address already in use :::3000\"); })'",
            "category": "Networking & Daemon",
            "description": "Simulates an orphaned background process occupying TCP port 3000."
        },
        {
            "id": "missing-module",
            "name": "Missing Module Wraith (ImportError)",
            "command": "python -c 'import torch; print(torch.__version__)'",
            "category": "Dependency Haunting",
            "description": "Simulates calling an uninstalled heavy deep learning dependency in an isolated environment."
        },
        {
            "id": "oom-reaper",
            "name": "OOM Reaper (Exit Code 137)",
            "command": "bash -c 'echo \"FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed - JavaScript heap out of memory\"; exit 137'",
            "category": "Resource Exhaustion",
            "description": "Simulates a process killed by the OOM supervisor due to excessive heap allocation."
        },
        {
            "id": "segfault-spectre",
            "name": "Memory Corruption Spectre (SIGSEGV 139)",
            "command": "bash -c 'echo \"Segmentation fault (core dumped)\"; exit 139'",
            "category": "Native Memory Fault",
            "description": "Simulates a hardware memory access violation or null pointer dereference."
        },
        {
            "id": "git-divergence",
            "name": "Temporal Divergence (Git Conflict)",
            "command": "git merge ghost-branch",
            "category": "Version Control",
            "description": "Simulates overlapping branch changes and unmerged conflict hunks."
        }
    ]
