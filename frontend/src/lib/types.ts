export interface SuspectProfile {
  id: string;
  name: string;
  role_title: string;
  status: string;
  tagline: string;
  avatar_ascii: string;
  alibi: string;
  tension_level: number;
}

export interface EvidenceItem {
  id: string;
  title: string;
  file_path: string;
  category: string;
  badge: string;
  description: string;
  raw_content: string;
  forensic_hint: string;
}

export interface CaseDossier {
  case_number: string;
  case_title: string;
  victim: string;
  time_of_death: string;
  location: string;
  briefing: string;
  suspects: SuspectProfile[];
  evidence_locker: EvidenceItem[];
}

export interface ChatMessage {
  id: string;
  role: "detective" | "suspect" | "system";
  sender: string;
  content: string;
  timestamp: string;
  presentedEvidence?: string;
  glitch?: boolean;
}

export interface InterrogateResponse {
  suspect_id: string;
  suspect_name: string;
  reply: string;
  tension_level: number;
  glitch_intensity: number;
  revealed_clue?: string;
  model_used: string;
  offline_mode: boolean;
  timestamp: string;
}

export interface IndictmentResponse {
  verdict: "GUILTY_EXORCISED" | "PARTIAL_EXORCISM" | "WRONGFUL_CONVICTION";
  success: boolean;
  score: number;
  detective_rank: string;
  title: string;
  narrative: string;
  breakdown: Record<string, string>;
  timestamp: string;
}

export interface SystemStatus {
  app_name: string;
  version: string;
  tagline: string;
  model_configured: string;
  ollama_endpoint: string;
  ollama_reachable: boolean;
  offline_fallback_active: boolean;
  total_incidents_recorded: number;
  airgap_verified: boolean;
}
