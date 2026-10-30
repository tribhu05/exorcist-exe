from fastapi import APIRouter, HTTPException
from app.models.schemas import CommandAutopsyRequest, CommandAutopsyResponse
from app.services.llm_engine import llm_engine
from app.services.grimoire_store import grimoire_store

router = APIRouter(prefix="/api/autopsy", tags=["Autopsy"])

@router.post("", response_model=CommandAutopsyResponse)
async def autopsy_command(req: CommandAutopsyRequest):
    try:
        autopsy = await llm_engine.autopsy_command(
            command=req.command,
            exit_code=req.exit_code,
            stdout=req.stdout or "",
            stderr=req.stderr or "",
            cwd=req.cwd
        )

        # Record in Grimoire if an anomaly was detected
        if autopsy.status == "anomaly_detected":
            grimoire_store.record_incident(
                incident_id=autopsy.incident_id,
                incident_type="COMMAND_AUTOPSY",
                title=f"{autopsy.ghost_type} ({req.command})",
                severity=autopsy.severity,
                details=autopsy.model_dump()
            )

        return autopsy
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Spectral autopsy failed: {str(e)}")
