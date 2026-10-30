from fastapi import APIRouter, HTTPException
from app.models.game_schemas import (
    CaseDossier,
    InterrogateRequest,
    InterrogateResponse,
    IndictmentRequest,
    IndictmentResponse,
    EvidenceItem
)
from app.services.game_engine import game_engine
from app.services.grimoire_store import grimoire_store

router = APIRouter(prefix="/api/game", tags=["Exorcist Game"])

@router.get("/case", response_model=CaseDossier)
async def get_case_dossier():
    return game_engine.get_dossier()

@router.post("/interrogate", response_model=InterrogateResponse)
async def interrogate_suspect(req: InterrogateRequest):
    try:
        response = await game_engine.interrogate(
            suspect_id=req.suspect_id,
            message=req.message,
            presented_evidence_id=req.presented_evidence_id,
            history=req.history
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interrogation failed: {str(e)}")

@router.post("/indict", response_model=IndictmentResponse)
async def submit_indictment(req: IndictmentRequest):
    try:
        verdict = game_engine.evaluate_indictment(req)

        # Log into Grimoire
        grimoire_store.record_incident(
            incident_id=f"CASE1031-{verdict.verdict}",
            incident_type="CASE_INDICTMENT",
            title=f"{verdict.title} ({verdict.detective_rank})",
            severity="LOW" if verdict.success else "CRITICAL",
            details=verdict.model_dump()
        )

        return verdict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indictment evaluation failed: {str(e)}")

@router.get("/evidence/{evidence_id}", response_model=EvidenceItem)
async def get_evidence_item(evidence_id: str):
    dossier = game_engine.get_dossier()
    item = next((e for e in dossier.evidence_locker if e.id == evidence_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Evidence file not found in forensic locker")
    return item
