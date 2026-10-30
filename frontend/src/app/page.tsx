"use client";

import React, { useState, useEffect } from "react";
import Navbar from "@/components/Navbar";
import SuspectCard from "@/components/SuspectCard";
import EvidenceViewer from "@/components/EvidenceViewer";
import InterrogationRoom from "@/components/InterrogationRoom";
import IndictmentModal from "@/components/IndictmentModal";
import { fetchCaseDossier } from "@/lib/api";
import { CaseDossier, SuspectProfile, EvidenceItem } from "@/lib/types";
import { Terminal, Shield, Sparkles, Cpu, BookOpen, AlertOctagon } from "lucide-react";

export default function ForensicDetectiveDashboard() {
  const [dossier, setDossier] = useState<CaseDossier | null>(null);
  const [activeSuspect, setActiveSuspect] = useState<SuspectProfile | null>(null);
  const [presentedEvidence, setPresentedEvidence] = useState<EvidenceItem | null>(null);
  const [crtEnabled, setCrtEnabled] = useState(true);
  const [isIndictmentOpen, setIsIndictmentOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await fetchCaseDossier();
        setDossier(data);
        if (data.suspects.length > 0) {
          setActiveSuspect(data.suspects[3] || data.suspects[0]); // Default to Daemon 666 or first
        }
      } catch (err) {
        console.error("Error loading case dossier:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleUpdateSuspectTension = (suspectId: string, newTension: number) => {
    if (!dossier) return;
    setDossier((prev) => {
      if (!prev) return prev;
      return {
        ...prev,
        suspects: prev.suspects.map((s) =>
          s.id === suspectId ? { ...s, tension_level: newTension } : s
        ),
      };
    });
    if (activeSuspect && activeSuspect.id === suspectId) {
      setActiveSuspect((prev) => (prev ? { ...prev, tension_level: newTension } : null));
    }
  };

  if (loading || !dossier) {
    return (
      <div className="min-h-screen bg-[#080d0a] text-[#00ff66] flex flex-col items-center justify-center font-mono">
        <Terminal className="h-10 w-10 animate-spin mb-4" />
        <p className="tracking-widest text-sm">INITIALIZING CRIME LAB // DECRYPTING RING 0 COREDUMP...</p>
      </div>
    );
  }

  return (
    <div className={`min-h-screen bg-[#080d0a] text-[#e7f0e9] font-mono flex flex-col ${crtEnabled ? "crt-flicker" : ""}`}>
      {/* CRT Scanline and Vignette Overlays */}
      {crtEnabled && (
        <>
          <div className="crt-overlay" />
          <div className="crt-vignette" />
        </>
      )}

      {/* Navigation */}
      <Navbar
        crtEnabled={crtEnabled}
        onToggleCrt={() => setCrtEnabled(!crtEnabled)}
        onOpenIndictment={() => setIsIndictmentOpen(true)}
      />

      {/* Case Briefing Strip */}
      <section className="bg-[#0e1711] border-b border-[#1b3523] px-4 py-3">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4 text-xs">
          <div className="flex items-center gap-3">
            <span className="px-2 py-0.5 rounded bg-[#ff4444]/20 text-[#ff4444] border border-[#ff4444]/40 font-bold uppercase flex items-center gap-1">
              <AlertOctagon className="h-3 w-3" /> CRIME SCENE: RING 0
            </span>
            <span className="text-[#89978d]">VICTIM: <strong className="text-[#e7f0e9]">{dossier.victim}</strong></span>
            <span className="hidden sm:inline text-[#89978d]">TIME OF DEATH: <strong className="text-[#ffb000]">{dossier.time_of_death}</strong></span>
          </div>

          <div className="flex items-center gap-3 text-[11px] text-[#89978d]">
            <span className="flex items-center gap-1 text-[#00ff66]">
              <Shield className="h-3.5 w-3.5" /> AIR-GAP VERIFIED (0 BYTES EGRESS)
            </span>
            <span className="hidden md:inline">•</span>
            <span className="hidden md:inline text-[#ffb000]">
              OLLAMA + LOCAL OPEN-WEIGHTS (GEMMA 2 / LLAMA 3.2)
            </span>
          </div>
        </div>
      </section>

      {/* Main Forensic Workstation Grid */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Column: Suspect Lineup & Evidence Locker (7 Cols) */}
        <div className="lg:col-span-7 flex flex-col gap-5">
          {/* Suspect Lineup */}
          <div>
            <div className="flex items-center justify-between mb-2.5">
              <div className="flex items-center gap-2">
                <Cpu className="h-4 w-4 text-[#00ff66]" />
                <h2 className="text-sm font-bold text-[#e7f0e9] uppercase tracking-wider">
                  SUSPECT DAEMONS IN CUSTODY (CHOOSE TO INTERROGATE)
                </h2>
              </div>
              <span className="text-[11px] text-[#89978d]">4 System Processes Detained</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {dossier.suspects.map((suspect) => (
                <SuspectCard
                  key={suspect.id}
                  suspect={suspect}
                  isSelected={activeSuspect?.id === suspect.id}
                  onSelect={(s) => setActiveSuspect(s)}
                />
              ))}
            </div>
          </div>

          {/* Forensic Evidence Locker */}
          <div className="flex-1">
            <EvidenceViewer
              evidenceList={dossier.evidence_locker}
              onPresentEvidence={(item) => setPresentedEvidence(item)}
              activeSuspectName={activeSuspect?.name}
            />
          </div>
        </div>

        {/* Right Column: Active Interrogation Chamber (5 Cols) */}
        <div className="lg:col-span-5 h-[620px] lg:h-auto flex flex-col">
          {activeSuspect ? (
            <InterrogationRoom
              suspect={activeSuspect}
              presentedEvidence={presentedEvidence}
              onClearPresentedEvidence={() => setPresentedEvidence(null)}
              onUpdateSuspectTension={handleUpdateSuspectTension}
            />
          ) : (
            <div className="h-full rounded-lg border border-[#1b3523] bg-[#090f0b] flex flex-col items-center justify-center p-6 text-center text-[#89978d]">
              <Cpu className="h-8 w-8 mb-2 text-[#00ff66]" />
              <p>Select a suspect process from the lineup to begin the interrogation.</p>
            </div>
          )}
        </div>
      </main>

      {/* Terminal CLI Hint & Hacktoberfest Footer */}
      <footer className="border-t border-[#1b3523] bg-[#070b09] px-4 py-4 mt-6">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4 text-xs text-[#89978d]">
          {/* CLI Instructions */}
          <div className="flex items-center gap-2 bg-[#0e1611] border border-[#1b3523] px-3 py-1.5 rounded">
            <Terminal className="h-4 w-4 text-[#00ff66]" />
            <span>PLAY IN TERMINAL:</span>
            <code className="text-[#00ff66] font-bold">python cli/detective.py</code>
          </div>

          {/* Hacktoberfest Theme */}
          <div className="flex items-center gap-2 text-[11px]">
            <Sparkles className="h-3.5 w-3.5 text-[#ffb000]" />
            <span>Hacktoberfest 2026 Week 4: <strong className="text-[#e7f0e9]">&ldquo;Ghost in the Machine&rdquo;</strong></span>
          </div>

          {/* Open-Source Innovation */}
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1 text-[#00ff66]">
              <BookOpen className="h-3.5 w-3.5" /> 100% Open-Source & Air-Gapped AI
            </span>
          </div>
        </div>
      </footer>

      {/* Indictment & Exorcism Modal */}
      <IndictmentModal
        isOpen={isIndictmentOpen}
        onClose={() => setIsIndictmentOpen(false)}
        suspects={dossier.suspects}
      />
    </div>
  );
}
