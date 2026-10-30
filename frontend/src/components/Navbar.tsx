"use client";

import React, { useState, useEffect } from "react";
import { Terminal, Volume2, VolumeX, Monitor, ShieldCheck, AlertTriangle } from "lucide-react";
import { cyberAudio } from "@/lib/audio";

interface NavbarProps {
  crtEnabled: boolean;
  onToggleCrt: () => void;
  onOpenIndictment: () => void;
}

export default function Navbar({ crtEnabled, onToggleCrt, onOpenIndictment }: NavbarProps) {
  const [secondsLeft, setSecondsLeft] = useState(899); // 14:59
  const [isMuted, setIsMuted] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => {
      setSecondsLeft((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  const toggleMute = () => {
    const next = !isMuted;
    setIsMuted(next);
    cyberAudio.isMuted = next;
    if (!next) cyberAudio.playKeyClick();
  };

  return (
    <header className="border-b border-[#1b3523] bg-[#0a110c]/90 backdrop-blur sticky top-0 z-50 px-4 py-3 flex flex-wrap items-center justify-between gap-4">
      {/* Brand & Case */}
      <div className="flex items-center gap-3">
        <div className="h-9 w-9 rounded border border-[#00ff66]/40 bg-[#00ff66]/10 flex items-center justify-center text-[#00ff66]">
          <Terminal className="h-5 w-5" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="font-bold text-[#00ff66] tracking-wider text-base">EXORCIST.EXE</span>
            <span className="text-xs px-1.5 py-0.5 rounded bg-[#ffb000]/20 text-[#ffb000] border border-[#ffb000]/40 font-mono">
              CASE #1031
            </span>
          </div>
          <p className="text-xs text-[#89978d] font-mono">Digital Coroner // The Murder of PID 1</p>
        </div>
      </div>

      {/* Watchdog Timer & Controls */}
      <div className="flex items-center gap-3 sm:gap-6 flex-wrap">
        {/* Watchdog Timer */}
        <div className="flex items-center gap-2 bg-[#101a14] border border-[#223e2c] px-3 py-1.5 rounded">
          <AlertTriangle className="h-4 w-4 text-[#ffb000] animate-pulse" />
          <div className="text-xs font-mono">
            <span className="text-[#89978d] block text-[10px]">WATCHDOG TIMER</span>
            <span className={`font-bold tracking-widest ${secondsLeft < 300 ? "text-[#ff4444]" : "text-[#ffb000]"}`}>
              {formatTime(secondsLeft)}
            </span>
          </div>
        </div>

        {/* Airgap Status */}
        <div className="hidden md:flex items-center gap-1.5 text-xs text-[#00ff66] bg-[#00ff66]/10 border border-[#00ff66]/30 px-2.5 py-1.5 rounded font-mono">
          <ShieldCheck className="h-3.5 w-3.5" />
          <span>100% AIR-GAPPED</span>
        </div>

        {/* CRT Toggle */}
        <button
          onClick={() => {
            cyberAudio.playKeyClick();
            onToggleCrt();
          }}
          className={`px-2.5 py-1.5 rounded border text-xs font-mono flex items-center gap-1.5 transition-colors ${
            crtEnabled
              ? "bg-[#00ff66]/20 border-[#00ff66] text-[#00ff66]"
              : "bg-[#101a14] border-[#223e2c] text-[#89978d] hover:text-[#e7f0e9]"
          }`}
          title="Toggle CRT Scanline Effect"
        >
          <Monitor className="h-3.5 w-3.5" />
          <span className="hidden sm:inline">CRT FX</span>
        </button>

        {/* Audio Toggle */}
        <button
          onClick={toggleMute}
          className={`p-1.5 rounded border text-xs transition-colors ${
            !isMuted
              ? "bg-[#00ff66]/20 border-[#00ff66] text-[#00ff66]"
              : "bg-[#101a14] border-[#223e2c] text-[#89978d] hover:text-[#e7f0e9]"
          }`}
          title={isMuted ? "Unmute Sound" : "Mute Sound"}
        >
          {isMuted ? <VolumeX className="h-4 w-4" /> : <Volume2 className="h-4 w-4" />}
        </button>

        {/* Indict Button */}
        <button
          onClick={() => {
            cyberAudio.playTerminalBeep();
            onOpenIndictment();
          }}
          className="bg-[#ff4444] hover:bg-[#ff2222] text-white px-3.5 py-1.5 rounded font-mono text-xs font-bold tracking-wider uppercase shadow-[0_0_15px_rgba(255,68,68,0.4)] transition-all animate-pulse"
        >
          EXORCISE & INDICT
        </button>
      </div>
    </header>
  );
}
