"use client";

import React from "react";
import { SuspectProfile } from "@/lib/types";
import { cyberAudio } from "@/lib/audio";
import { ShieldAlert, User, Cpu } from "lucide-react";

interface SuspectCardProps {
  suspect: SuspectProfile;
  isSelected: boolean;
  onSelect: (suspect: SuspectProfile) => void;
}

export default function SuspectCard({ suspect, isSelected, onSelect }: SuspectCardProps) {
  const tension = suspect.tension_level;
  const tensionColor = tension < 40 ? "text-[#00ff66]" : tension < 75 ? "text-[#ffb000]" : "text-[#ff4444]";
  const tensionBg = tension < 40 ? "bg-[#00ff66]" : tension < 75 ? "bg-[#ffb000]" : "bg-[#ff4444]";

  return (
    <div
      onClick={() => {
        cyberAudio.playKeyClick();
        onSelect(suspect);
      }}
      className={`cursor-pointer rounded-lg border p-4 transition-all duration-200 relative overflow-hidden flex flex-col justify-between ${
        isSelected
          ? "border-[#00ff66] bg-[#0c1a11] shadow-[0_0_20px_rgba(0,255,102,0.15)]"
          : "border-[#1b3523] bg-[#0d1510] hover:border-[#2d583b] hover:bg-[#101c14]"
      }`}
    >
      {/* Header */}
      <div>
        <div className="flex items-start justify-between gap-2 mb-2">
          <div className="flex items-center gap-2">
            <Cpu className="h-4 w-4 text-[#00ff66]" />
            <h3 className="font-mono font-bold text-sm text-[#e7f0e9]">{suspect.name}</h3>
          </div>
          <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-[#16271c] text-[#89978d] border border-[#23422e]">
            {suspect.role_title}
          </span>
        </div>

        {/* ASCII Avatar */}
        <pre className="font-mono text-[10px] text-[#00ff66] bg-[#070b09] p-2 rounded border border-[#182e1f] my-2 select-none overflow-x-auto whitespace-pre leading-tight">
          {suspect.avatar_ascii.trim()}
        </pre>

        {/* Tagline */}
        <p className="text-xs text-[#89978d] italic font-mono mb-3 line-clamp-2">
          &ldquo;{suspect.tagline}&rdquo;
        </p>
      </div>

      {/* Tension Meter & Status */}
      <div className="pt-2 border-t border-[#182e1f]">
        <div className="flex items-center justify-between text-xs font-mono mb-1">
          <span className="text-[#89978d] text-[10px] flex items-center gap-1">
            <ShieldAlert className="h-3 w-3" /> TENSION METER
          </span>
          <span className={`font-bold ${tensionColor}`}>{tension}%</span>
        </div>
        <div className="w-full bg-[#16241a] h-1.5 rounded-full overflow-hidden">
          <div
            className={`h-full transition-all duration-500 ${tensionBg}`}
            style={{ width: `${tension}%` }}
          />
        </div>

        {/* Button */}
        <button
          className={`w-full mt-3 py-1.5 px-3 rounded text-xs font-mono font-semibold transition-colors flex items-center justify-center gap-1.5 ${
            isSelected
              ? "bg-[#00ff66] text-[#080d0a]"
              : "bg-[#182e1f] text-[#00ff66] hover:bg-[#22442d]"
          }`}
        >
          <User className="h-3.5 w-3.5" />
          {isSelected ? "INTERROGATING ACTIVE" : "INTERROGATE"}
        </button>
      </div>
    </div>
  );
}
