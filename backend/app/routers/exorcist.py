from fastapi import APIRouter, HTTPException
import uuid
from app.models.schemas import ExorcismRequest, ExorcismResponse
from app.services.llm_engine import llm_engine
from app.services.grimoire_store import grimoire_store

router = APIRouter(prefix="/api/exorcist", tags=["Exorcist"])

@router.post("", response_model=ExorcismResponse)
async def exorcise_code(req: ExorcismRequest):
    try:
        exorcism = await llm_engine.exorcise_code(
            code=req.code,
            filename=req.filename or "snippet.py",
            language=req.language or "python"
        )

        # Record in Grimoire if anomalies found
        if exorcism.anomalies_found:
            incident_id = f"EXORCISM-{uuid.uuid4().hex[:8].upper()}"
            grimoire_store.record_incident(
                incident_id=incident_id,
                incident_type="CODE_EXORCISM",
                title=f"Haunted code in {exorcism.file_analyzed} ({len(exorcism.anomalies_found)} anomalies)",
                severity="HIGH" if exorcism.haunted_score > 50 else "MEDIUM",
                details=exorcism.model_dump()
            )

        return exorcism
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code exorcism failed: {str(e)}")
