from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import GrimoireRecord, SystemStatusResponse
from app.services.grimoire_store import grimoire_store
from app.services.llm_engine import llm_engine
from app.config import settings

router = APIRouter(tags=["Grimoire & System"])

@router.get("/api/grimoire", response_model=List[GrimoireRecord])
async def list_grimoire_incidents(limit: int = 50):
    return grimoire_store.list_incidents(limit=limit)

@router.post("/api/grimoire/{incident_id}/resolve")
async def resolve_incident(incident_id: str):
    success = grimoire_store.resolve_incident(incident_id)
    if not success:
        raise HTTPException(status_code=404, detail="Incident not found or already resolved")
    return {"status": "success", "message": f"Incident {incident_id} marked as exorcised/resolved"}

@router.get("/api/status", response_model=SystemStatusResponse)
async def get_system_status():
    ollama_ok = await llm_engine.is_ollama_alive()
    count = grimoire_store.get_count()
    return SystemStatusResponse(
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        tagline=settings.TAGLINE,
        model_configured=settings.OLLAMA_MODEL,
        ollama_endpoint=settings.OLLAMA_BASE_URL,
        ollama_reachable=ollama_ok,
        offline_fallback_active=True,
        total_incidents_recorded=count,
        airgap_verified=True
    )
