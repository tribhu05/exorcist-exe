"use client";

import React, { useState, useRef, useEffect } from "react";
import { SuspectProfile, ChatMessage, EvidenceItem } from "@/lib/types";
import { sendInterrogation } from "@/lib/api";
import { cyberAudio } from "@/lib/audio";
import { Send, Sparkles, MessageSquare, ShieldAlert, Cpu } from "lucide-react";

interface InterrogationRoomProps {
  suspect: SuspectProfile;
  presentedEvidence: EvidenceItem | null;
  onClearPresentedEvidence: () => void;
  onUpdateSuspectTension: (suspectId: string, newTension: number) => void;
}

const QUICK_INQUIRIES = [
  "Where were you at 03:42:19 UTC?",
  "What process bound raw socket 666?",
  "Did you touch PID 1's stack buffer?",
  "Who authorized the rogue cgroup?",
];

export default function InterrogationRoom({
  suspect,
  presentedEvidence,
  onClearPresentedEvidence,
  onUpdateSuspectTension,
}: InterrogationRoomProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "intro-1",
      role: "system",
      sender: "CONSOLE",
      content: `Interrogation link initialized with ${suspect.name}. Watchdog recording active.`,
      timestamp: new Date().toLocaleTimeString(),
    },
    {
      id: "intro-2",
      role: "suspect",
      sender: suspect.name,
      content: `"${suspect.tagline}" What do you want, Detective? I have an operating system to maintain.`,
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);

  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  // When presented evidence changes externally, auto-suggest or trigger
  useEffect(() => {
    if (presentedEvidence) {
      handleSend(`Explain this evidence found at the crime scene: ${presentedEvidence.title}!`);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [presentedEvidence]);

  const handleSend = async (messageText?: string) => {
    const textToSend = messageText || input;
    if (!textToSend.trim() || isTyping) return;

    cyberAudio.playTerminalBeep();

    const userMsg: ChatMessage = {
      id: `usr-${Date.now()}`,
      role: "detective",
      sender: "DETECTIVE RAY TRACE",
      content: textToSend,
      timestamp: new Date().toLocaleTimeString(),
      presentedEvidence: presentedEvidence?.title,
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!messageText) setInput("");
    setIsTyping(true);

    try {
      const res = await sendInterrogation(
        suspect.id,
        textToSend,
        presentedEvidence?.id
      );

      // Play audio based on tension
      if (res.tension_level > 70) {
        cyberAudio.playGlitchStatic();
      } else {
        cyberAudio.playTerminalBeep();
      }

      onUpdateSuspectTension(suspect.id, res.tension_level);

      const replyMsg: ChatMessage = {
        id: `reply-${Date.now()}`,
        role: "suspect",
        sender: res.suspect_name,
        content: res.reply,
        timestamp: new Date().toLocaleTimeString(),
        glitch: res.glitch_intensity > 0.5,
      };

      setMessages((prev) => [...prev, replyMsg]);

      if (res.revealed_clue) {
        setMessages((prev) => [
          ...prev,
          {
            id: `clue-${Date.now()}`,
            role: "system",
            sender: "CRIME LOG",
            content: `CRITICAL BREAKTHROUGH: ${res.revealed_clue}`,
            timestamp: new Date().toLocaleTimeString(),
          },
        ]);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: `err-${Date.now()}`,
          role: "system",
          sender: "SYSTEM",
          content: "Interrogation link glitched. The process refused to answer.",
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
    } finally {
      setIsTyping(false);
      onClearPresentedEvidence();
    }
  };

  const isGlitching = suspect.tension_level > 75;

  return (
    <div className="rounded-lg border border-[#1b3523] bg-[#090f0b] flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="bg-[#0f1a13] px-4 py-3 border-b border-[#1b3523] flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded border border-[#00ff66]/30 bg-[#00ff66]/10 flex items-center justify-center text-[#00ff66]">
            <Cpu className="h-4 w-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className={`font-mono font-bold text-sm text-[#e7f0e9] ${isGlitching ? "glitch-active text-[#ff4444]" : ""}`}>
                {suspect.name}
              </h3>
              <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-[#1b3523] text-[#00ff66] border border-[#2d583b]">
                {suspect.role_title}
              </span>
            </div>
            <p className="text-[11px] text-[#89978d] font-mono italic">
              Status: {suspect.status}
            </p>
          </div>
        </div>

        {/* Tension Meter */}
        <div className="flex items-center gap-3">
          <div className="text-right">
            <span className="text-[10px] font-mono text-[#89978d] block flex items-center justify-end gap-1">
              <ShieldAlert className="h-3 w-3 text-[#ffb000]" /> TENSION
            </span>
            <span className={`font-mono text-xs font-bold ${
              suspect.tension_level < 40 ? "text-[#00ff66]" : suspect.tension_level < 75 ? "text-[#ffb000]" : "text-[#ff4444]"
            }`}>
              {suspect.tension_level}%
            </span>
          </div>
          <div className="w-16 sm:w-24 bg-[#142218] h-2 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-300 ${
                suspect.tension_level < 40 ? "bg-[#00ff66]" : suspect.tension_level < 75 ? "bg-[#ffb000]" : "bg-[#ff4444]"
              }`}
              style={{ width: `${suspect.tension_level}%` }}
            />
          </div>
        </div>
      </div>

      {/* Presented Clue Banner */}
      {presentedEvidence && (
        <div className="bg-[#ffb000]/15 border-b border-[#ffb000]/40 px-4 py-2 flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-mono text-[#ffb000]">
            <Sparkles className="h-3.5 w-3.5 animate-spin" />
            <span>SLAMMING CLUE ON TABLE: <strong>{presentedEvidence.title}</strong></span>
          </div>
          <button
            onClick={onClearPresentedEvidence}
            className="text-[10px] font-mono text-[#89978d] hover:text-[#e7f0e9] underline"
          >
            Cancel
          </button>
        </div>
      )}

      {/* Messages Stream */}
      <div className="flex-1 p-4 overflow-y-auto space-y-3 font-mono text-xs">
        {messages.map((m) => {
          if (m.role === "system") {
            return (
              <div key={m.id} className="text-center my-2">
                <span className="inline-block px-3 py-1 rounded bg-[#152319] border border-[#23422e] text-[#ffb000] text-[11px]">
                  {m.content}
                </span>
              </div>
            );
          }

          const isUser = m.role === "detective";
          return (
            <div
              key={m.id}
              className={`flex flex-col ${isUser ? "items-end" : "items-start"}`}
            >
              <div className="flex items-center gap-2 mb-1">
                <span className={`text-[10px] font-bold ${isUser ? "text-[#00ff66]" : "text-[#ffb000]"}`}>
                  {m.sender}
                </span>
                <span className="text-[10px] text-[#55695c]">{m.timestamp}</span>
              </div>

              {m.presentedEvidence && (
                <div className="mb-1 text-[10px] bg-[#ffb000]/20 text-[#ffb000] border border-[#ffb000]/40 px-2 py-0.5 rounded">
                  [Confronted with: {m.presentedEvidence}]
                </div>
              )}

              <div
                className={`p-3 rounded-lg max-w-[85%] leading-relaxed ${
                  isUser
                    ? "bg-[#13271b] border border-[#22442d] text-[#e7f0e9]"
                    : "bg-[#0b140f] border border-[#1b3523] text-[#a0b8a6]"
                } ${m.glitch ? "glitch-active border-[#ff4444]" : ""}`}
              >
                {m.content}
              </div>
            </div>
          );
        })}

        {isTyping && (
          <div className="flex items-center gap-2 text-xs text-[#89978d] italic py-2">
            <span className="h-2 w-2 rounded-full bg-[#00ff66] animate-ping" />
            <span>{suspect.name} is processing instruction registers...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompt Chips */}
      <div className="px-4 py-2 border-t border-[#18291d] bg-[#0c140f] flex gap-2 overflow-x-auto">
        <span className="text-[10px] text-[#89978d] font-mono shrink-0 flex items-center gap-1">
          <MessageSquare className="h-3 w-3" /> Quick Inquiries:
        </span>
        {QUICK_INQUIRIES.map((q, i) => (
          <button
            key={i}
            onClick={() => handleSend(q)}
            disabled={isTyping}
            className="text-[11px] font-mono px-2.5 py-1 rounded bg-[#132218] border border-[#23422e] text-[#e7f0e9] hover:border-[#00ff66] hover:text-[#00ff66] whitespace-nowrap transition-colors"
          >
            {q}
          </button>
        ))}
      </div>

      {/* Input Deck */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="p-3 border-t border-[#1b3523] bg-[#090f0b] flex gap-2"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => {
            cyberAudio.playKeyClick();
            setInput(e.target.value);
          }}
          placeholder={`Interrogate ${suspect.name}...`}
          disabled={isTyping}
          className="flex-1 bg-[#050806] border border-[#1b3523] rounded px-3 py-2 text-xs font-mono text-[#e7f0e9] placeholder-[#4f6456] focus:outline-none focus:border-[#00ff66]"
        />
        <button
          type="submit"
          disabled={!input.trim() || isTyping}
          className="bg-[#00ff66] hover:bg-[#20ff78] disabled:opacity-40 text-[#080d0a] font-mono font-bold px-4 py-2 rounded text-xs flex items-center gap-1.5 transition-all"
        >
          <Send className="h-3.5 w-3.5" />
          <span>TRANSMIT</span>
        </button>
      </form>
    </div>
  );
}
