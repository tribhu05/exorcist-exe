"use client";

import React, { useState } from "react";
import { EvidenceItem } from "@/lib/types";
import { cyberAudio } from "@/lib/audio";
import { FolderLock, FileText, Search, Sparkles } from "lucide-react";

interface EvidenceViewerProps {
  evidenceList: EvidenceItem[];
  onPresentEvidence?: (item: EvidenceItem) => void;
  activeSuspectName?: string;
}

export default function EvidenceViewer({ evidenceList, onPresentEvidence, activeSuspectName }: EvidenceViewerProps) {
  const [selectedEvidenceId, setSelectedEvidenceId] = useState<string>(evidenceList[0]?.id || "");

  const activeItem = evidenceList.find((e) => e.id === selectedEvidenceId) || evidenceList[0];

  return (
    <div className="rounded-lg border border-[#1b3523] bg-[#0c140f] p-4 flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-[#1b3523] mb-3">
        <div className="flex items-center gap-2">
          <FolderLock className="h-4 w-4 text-[#ffb000]" />
          <h2 className="font-mono font-bold text-sm text-[#e7f0e9] tracking-wider uppercase">
            FORENSIC EVIDENCE LOCKER
          </h2>
        </div>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#ffb000]/20 text-[#ffb000] border border-[#ffb000]/40">
          {evidenceList.length} FILES RETRIEVED
        </span>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 overflow-x-auto pb-2 mb-3">
        {evidenceList.map((item) => (
          <button
            key={item.id}
            onClick={() => {
              cyberAudio.playKeyClick();
              setSelectedEvidenceId(item.id);
            }}
            className={`px-3 py-1.5 rounded text-xs font-mono whitespace-nowrap transition-all border flex items-center gap-1.5 ${
              item.id === selectedEvidenceId
                ? "bg-[#00ff66]/15 border-[#00ff66] text-[#00ff66] font-bold shadow-[0_0_10px_rgba(0,255,102,0.1)]"
                : "bg-[#111c15] border-[#1d3523] text-[#89978d] hover:text-[#e7f0e9]"
            }`}
          >
            <FileText className="h-3 w-3" />
            <span>{item.title.split("(")[0]}</span>
          </button>
        ))}
      </div>

      {/* Active Evidence Body */}
      {activeItem && (
        <div className="flex-1 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between gap-2 mb-1.5">
              <span className="text-xs font-mono text-[#00ff66] font-bold">{activeItem.file_path}</span>
              <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-[#ff4444]/20 text-[#ff4444] border border-[#ff4444]/40">
                {activeItem.badge}
              </span>
            </div>
            <p className="text-xs text-[#89978d] font-mono mb-3">{activeItem.description}</p>

            {/* Forensic Hint Banner */}
            <div className="bg-[#152319] border border-[#23422e] rounded p-2.5 mb-3 flex items-start gap-2">
              <Search className="h-4 w-4 text-[#ffb000] shrink-0 mt-0.5" />
              <p className="text-xs text-[#e7f0e9] font-mono">
                <strong className="text-[#ffb000]">CORONER HINT:</strong> {activeItem.forensic_hint}
              </p>
            </div>

            {/* Raw Terminal / Hex Content */}
            <div className="bg-[#050806] border border-[#18291d] rounded p-3 font-mono text-xs text-[#a0b0a5] overflow-x-auto max-h-56 leading-relaxed select-text whitespace-pre">
              {activeItem.raw_content}
            </div>
          </div>

          {/* Action button */}
          {onPresentEvidence && activeSuspectName && (
            <button
              onClick={() => {
                cyberAudio.playTerminalBeep();
                onPresentEvidence(activeItem);
              }}
              className="mt-3 w-full bg-[#ffb000]/20 hover:bg-[#ffb000]/30 text-[#ffb000] border border-[#ffb000]/60 py-2 rounded text-xs font-mono font-bold tracking-wider flex items-center justify-center gap-2 transition-all"
            >
              <Sparkles className="h-4 w-4" />
              CONFRONT {activeSuspectName.toUpperCase()} WITH THIS CLUE
            </button>
          )}
        </div>
      )}
    </div>
  );
}
