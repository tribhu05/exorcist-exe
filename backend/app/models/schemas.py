from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class CommandAutopsyRequest(BaseModel):
    command: str = Field(..., description="The command that was executed")
    exit_code: int = Field(..., description="The command process exit code")
    stdout: Optional[str] = Field(default="", description="Captured standard output")
    stderr: Optional[str] = Field(default="", description="Captured standard error")
    cwd: Optional[str] = Field(default=None, description="Working directory")
    environment: Optional[Dict[str, str]] = Field(default_factory=dict, description="Environment variables context")

class CommandAutopsyResponse(BaseModel):
    incident_id: str
    status: str
    ghost_type: str
    severity: str
    spectral_diagnosis: str
    root_cause: str
    suggested_command: Optional[str] = None
    patch_diff: Optional[str] = None
    explanation: str
    model_used: str
    offline_mode: bool
    timestamp: str

class HauntedAnomaly(BaseModel):
    id: str
    line_number: int
    end_line_number: Optional[int] = None
    ghost_pattern: str
    severity: str
    description: str
    original_snippet: str
    purified_snippet: str

class ExorcismRequest(BaseModel):
    code: str = Field(..., description="Source code to inspect and exorcise")
    filename: Optional[str] = Field(default="snippet.py", description="Filename or path")
    language: Optional[str] = Field(default="python", description="Programming language")

class ExorcismResponse(BaseModel):
    file_analyzed: str
    haunted_score: int
    anomalies_found: List[HauntedAnomaly]
    original_code: str
    purified_code: str
    unified_diff: str
    spectral_summary: str
    model_used: str
    offline_mode: bool
    timestamp: str

class ExecuteCommandRequest(BaseModel):
    command: str
    cwd: Optional[str] = None
    timeout: Optional[int] = 15

class ExecuteCommandResponse(BaseModel):
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: float
    autopsy: Optional[CommandAutopsyResponse] = None

class GrimoireRecord(BaseModel):
    id: str
    created_at: str
    incident_type: str
    title: str
    severity: str
    details: Dict[str, Any]
    resolved: bool = False

class SystemStatusResponse(BaseModel):
    app_name: str
    version: str
    tagline: str
    model_configured: str
    ollama_endpoint: str
    ollama_reachable: bool
    offline_fallback_active: bool
    total_incidents_recorded: int
    airgap_verified: bool
