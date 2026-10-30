from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SuspectProfile(BaseModel):
    id: str
    name: str
    role_title: str
    status: str
    tagline: str
    avatar_ascii: str
    alibi: str
    tension_level: int = 15

class EvidenceItem(BaseModel):
    id: str
    title: str
    file_path: str
    category: str
    badge: str
    description: str
    raw_content: str
    forensic_hint: str

class InterrogationMessage(BaseModel):
    role: str # "detective" | "suspect" | "system"
    content: str
    timestamp: str
    presented_evidence_id: Optional[str] = None

class InterrogateRequest(BaseModel):
    suspect_id: str
    message: str
    presented_evidence_id: Optional[str] = None
    history: Optional[List[InterrogationMessage]] = Field(default_factory=list)

class InterrogateResponse(BaseModel):
    suspect_id: str
    suspect_name: str
    reply: str
    tension_level: int
    glitch_intensity: float # 0.0 to 1.0 for visual glitching
    revealed_clue: Optional[str] = None
    model_used: str
    offline_mode: bool
    timestamp: str

class IndictmentRequest(BaseModel):
    accused_suspect_id: str
    murder_weapon: str
    exorcism_command: str
    notes: Optional[str] = ""

class IndictmentResponse(BaseModel):
    verdict: str # "GUILTY_EXORCISED" | "WRONGFUL_CONVICTION" | "KERNEL_PANIC"
    success: bool
    score: int
    detective_rank: str
    title: str
    narrative: str
    breakdown: Dict[str, Any]
    timestamp: str

class CaseDossier(BaseModel):
    case_number: str
    case_title: str
    victim: str
    time_of_death: str
    location: str
    briefing: str
    suspects: List[SuspectProfile]
    evidence_locker: List[EvidenceItem]
