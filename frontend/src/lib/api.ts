import { CaseDossier, InterrogateResponse, IndictmentResponse, SystemStatus } from "./types";
import { OFFLINE_DOSSIER, offlineInterrogate, offlineEvaluateIndictment } from "./offlineEngine";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchCaseDossier(): Promise<CaseDossier> {
  try {
    const res = await fetch(`${API_BASE}/api/game/case`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch case dossier");
    return await res.json();
  } catch (err) {
    console.warn("Using offline bundled dossier:", err);
    return OFFLINE_DOSSIER;
  }
}

export async function sendInterrogation(
  suspectId: string,
  message: string,
  presentedEvidenceId?: string
): Promise<InterrogateResponse> {
  try {
    const res = await fetch(`${API_BASE}/api/game/interrogate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        suspect_id: suspectId,
        message,
        presented_evidence_id: presentedEvidenceId || null,
      }),
    });
    if (!res.ok) throw new Error("Interrogation request failed");
    return await res.json();
  } catch (err) {
    console.warn("Falling back to local client dialogue matrix:", err);
    return offlineInterrogate(suspectId, message, presentedEvidenceId);
  }
}

export async function submitIndictment(
  accusedSuspectId: string,
  murderWeapon: string,
  exorcismCommand: string
): Promise<IndictmentResponse> {
  try {
    const res = await fetch(`${API_BASE}/api/game/indict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        accused_suspect_id: accusedSuspectId,
        murder_weapon: murderWeapon,
        exorcism_command: exorcismCommand,
      }),
    });
    if (!res.ok) throw new Error("Indictment request failed");
    return await res.json();
  } catch (err) {
    console.warn("Falling back to local client indictment evaluation:", err);
    return offlineEvaluateIndictment(accusedSuspectId, murderWeapon, exorcismCommand);
  }
}

export async function fetchSystemStatus(): Promise<SystemStatus> {
  try {
    const res = await fetch(`${API_BASE}/api/status`, { cache: "no-store" });
    if (!res.ok) throw new Error("Status failed");
    return await res.json();
  } catch {
    return {
      app_name: "EXORCIST.EXE // PHANTOM",
      version: "1.0.0",
      tagline: "The Ghost in your Terminal. Local. Offline. Omnipresent.",
      model_configured: "gemma2:2b",
      ollama_endpoint: "http://localhost:11434",
      ollama_reachable: false,
      offline_fallback_active: true,
      total_incidents_recorded: 4,
      airgap_verified: true
    };
  }
}
