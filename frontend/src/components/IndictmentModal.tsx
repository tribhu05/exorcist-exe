"use client";

import React, { useState } from "react";
import { SuspectProfile, IndictmentResponse } from "@/lib/types";
import { submitIndictment } from "@/lib/api";
import { cyberAudio } from "@/lib/audio";
import { X, Award, ShieldAlert, CheckCircle2, RotateCcw } from "lucide-react";

interface IndictmentModalProps {
  isOpen: boolean;
  onClose: () => void;
  suspects: SuspectProfile[];
}

const COMMON_WEAPONS = [
  "Buffer Overflow / Stack Smashing (0xDEADBEEF)",
  "Memory Leak & Unbounded Heap Accumulation",
  "Rogue Socket DMA Injection on Port 666",
  "Orphaned Fork Bomb & PID Exhaustion",
];

const PRESET_COMMANDS = [
  "kill -9 666",
  "sysctl -w kernel.randomize_va_space=2",
  "exorcise --pid 666 --force",
  "pkill -f systemd",
];

export default function IndictmentModal({ isOpen, onClose, suspects }: IndictmentModalProps) {
  const [selectedSuspectId, setSelectedSuspectId] = useState(suspects[3]?.id || suspects[0]?.id || "");
  const [murderWeapon, setMurderWeapon] = useState(COMMON_WEAPONS[0]);
  const [exorcismCommand, setExorcismCommand] = useState(PRESET_COMMANDS[0]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState<IndictmentResponse | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    cyberAudio.playTerminalBeep();

    try {
      const res = await submitIndictment(selectedSuspectId, murderWeapon, exorcismCommand);
      setResult(res);
      if (res.success) {
        cyberAudio.playVictory();
      } else {
        cyberAudio.playDefeat();
      }
    } catch {
      // Local fallback evaluation
      const isCorrect = selectedSuspectId === "phantom_socket";
      const fallbackRes: IndictmentResponse = {
        verdict: isCorrect ? "GUILTY_EXORCISED" : "WRONGFUL_CONVICTION",
        success: isCorrect,
        score: isCorrect ? 100 : 30,
        detective_rank: isCorrect ? "Grand Exorcist & Chief Digital Coroner" : "Junior Debugger",
        title: isCorrect ? "CASE SOLVED // THE MACHINE IS PURIFIED" : "WRONGFUL CONVICTION // KERNEL PANIC",
        narrative: isCorrect
          ? "You correctly identified Daemon 666 as the possessed process! The raw port 666 socket was terminated and Ring 0 memory restored."
          : "An innocent system daemon was killed while the true Ghost watching on port 666 escaped. The system crashed.",
        breakdown: {
          killer: isCorrect ? "Daemon 666 (CORRECT)" : "WRONG SUSPECT ACCUSED",
          exploit: murderWeapon,
          command_executed: exorcismCommand,
        },
        timestamp: new Date().toISOString(),
      };
      setResult(fallbackRes);
      if (isCorrect) cyberAudio.playVictory();
      else cyberAudio.playDefeat();
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleReset = () => {
    setResult(null);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-[#0b140f] border border-[#22442d] rounded-xl max-w-2xl w-full p-6 relative shadow-[0_0_50px_rgba(0,0,0,0.9)] font-mono">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-[#89978d] hover:text-[#e7f0e9] p-1.5 rounded"
        >
          <X className="h-5 w-5" />
        </button>

        {!result ? (
          <div>
            {/* Modal Header */}
            <div className="mb-6">
              <span className="text-[11px] uppercase tracking-widest text-[#ff4444] font-bold block mb-1">
                CRIME REPORT // OFFICIAL CHARGES
              </span>
              <h2 className="text-xl font-bold text-[#e7f0e9]">
                INDICTMENT & EXORCISM PROTOCOL
              </h2>
              <p className="text-xs text-[#89978d] mt-1">
                Name the process responsible for the murder of PID 1, specify the exploit weapon, and execute the terminal exorcism command.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Suspect Selection */}
              <div>
                <label className="block text-xs font-bold text-[#00ff66] mb-1.5 uppercase">
                  1. Accused Suspect
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {suspects.map((s) => (
                    <button
                      type="button"
                      key={s.id}
                      onClick={() => {
                        cyberAudio.playKeyClick();
                        setSelectedSuspectId(s.id);
                      }}
                      className={`p-3 rounded border text-left text-xs transition-all ${
                        selectedSuspectId === s.id
                          ? "bg-[#00ff66]/15 border-[#00ff66] text-[#00ff66] font-bold"
                          : "bg-[#111c15] border-[#1d3523] text-[#89978d] hover:text-[#e7f0e9]"
                      }`}
                    >
                      <div className="font-bold">{s.name}</div>
                      <div className="text-[10px] opacity-75">{s.role_title}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Murder Weapon / Mechanism */}
              <div>
                <label className="block text-xs font-bold text-[#ffb000] mb-1.5 uppercase">
                  2. Murder Exploit / Mechanism
                </label>
                <select
                  value={murderWeapon}
                  onChange={(e) => setMurderWeapon(e.target.value)}
                  className="w-full bg-[#050806] border border-[#1b3523] rounded px-3 py-2 text-xs text-[#e7f0e9] focus:outline-none focus:border-[#ffb000]"
                >
                  {COMMON_WEAPONS.map((w, idx) => (
                    <option key={idx} value={w} className="bg-[#0b140f]">
                      {w}
                    </option>
                  ))}
                </select>
              </div>

              {/* Exorcism Terminal Command */}
              <div>
                <label className="block text-xs font-bold text-[#ff4444] mb-1.5 uppercase">
                  3. Terminal Exorcism Command
                </label>
                <input
                  type="text"
                  value={exorcismCommand}
                  onChange={(e) => setExorcismCommand(e.target.value)}
                  placeholder="e.g. kill -9 666"
                  className="w-full bg-[#050806] border border-[#1b3523] rounded px-3 py-2 text-xs text-[#e7f0e9] focus:outline-none focus:border-[#ff4444]"
                />
                <div className="flex gap-2 mt-2">
                  <span className="text-[10px] text-[#89978d]">Presets:</span>
                  {PRESET_COMMANDS.map((cmd, i) => (
                    <button
                      type="button"
                      key={i}
                      onClick={() => setExorcismCommand(cmd)}
                      className="text-[10px] text-[#00ff66] hover:underline"
                    >
                      {cmd}
                    </button>
                  ))}
                </div>
              </div>

              {/* Submit */}
              <div className="pt-4 border-t border-[#1b3523]">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full bg-[#ff4444] hover:bg-[#ff2222] text-white py-3 rounded font-bold text-sm tracking-wider uppercase transition-all shadow-[0_0_20px_rgba(255,68,68,0.3)] flex items-center justify-center gap-2"
                >
                  <ShieldAlert className="h-4 w-4" />
                  <span>{isSubmitting ? "TRANSMITTING TO KERNEL..." : "EXECUTE EXORCISM INDICTMENT"}</span>
                </button>
              </div>
            </form>
          </div>
        ) : (
          /* Resolution View */
          <div className="text-center py-4">
            <div className="inline-flex p-3 rounded-full mb-3 bg-[#132419] border border-[#24422e]">
              {result.success ? (
                <Award className="h-10 w-10 text-[#00ff66] animate-bounce" />
              ) : (
                <ShieldAlert className="h-10 w-10 text-[#ff4444] animate-pulse" />
              )}
            </div>

            <span
              className={`text-xs uppercase tracking-widest font-bold block mb-1 ${
                result.success ? "text-[#00ff66]" : "text-[#ff4444]"
              }`}
            >
              {result.title}
            </span>

            <h3 className="text-2xl font-bold text-[#e7f0e9] mb-1">
              Score: {result.score}/100
            </h3>

            <p className="text-xs text-[#ffb000] font-bold uppercase mb-4">
              Detective Rank: {result.detective_rank}
            </p>

            <div className="bg-[#050806] border border-[#18291d] rounded-lg p-4 text-xs text-[#a0b8a6] text-left mb-4 leading-relaxed whitespace-pre-wrap">
              {result.narrative}
            </div>

            {/* Breakdown table */}
            <div className="bg-[#0d1611] border border-[#1b3523] rounded-lg p-3 text-left text-xs mb-6 space-y-1">
              <span className="text-[10px] text-[#89978d] uppercase tracking-wider block mb-1">
                Forensic Verification
              </span>
              {Object.entries(result.breakdown).map(([k, v]) => (
                <div key={k} className="flex justify-between border-b border-[#182b1e] pb-1">
                  <span className="text-[#89978d] capitalize">{k.replace(/_/g, " ")}:</span>
                  <span className={result.success ? "text-[#00ff66]" : "text-[#ff4444]"}>{v}</span>
                </div>
              ))}
            </div>

            <div className="flex gap-3">
              <button
                onClick={handleReset}
                className="flex-1 bg-[#13271b] hover:bg-[#1a3826] text-[#00ff66] border border-[#23472f] py-2.5 rounded text-xs font-bold transition-all flex items-center justify-center gap-2"
              >
                <RotateCcw className="h-4 w-4" />
                <span>TRY ANOTHER CASE THEORY</span>
              </button>
              <button
                onClick={onClose}
                className="flex-1 bg-[#00ff66] hover:bg-[#15e66d] text-[#080d0a] py-2.5 rounded text-xs font-bold transition-all flex items-center justify-center gap-2"
              >
                <CheckCircle2 className="h-4 w-4" />
                <span>CLOSE CASE DOSSIER</span>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
