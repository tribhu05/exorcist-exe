import os
import sys
import asyncio
import subprocess
import argparse
from typing import List, Tuple

DEFAULT_FFMPEG = r"C:\Python314\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
if os.path.exists(DEFAULT_FFMPEG):
    FFMPEG_EXE = DEFAULT_FFMPEG
else:
    try:
        import imageio_ffmpeg
        FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        FFMPEG_EXE = "ffmpeg"

SCRIPT_SEGMENTS: List[Tuple[float, str]] = [
    (
        1.5,
        "At 03:42:19 UTC, the central heartbeat of the operating system flatlined. "
        "PID 1—the parent of all processes—was struck down by a violent General Protection Fault. "
        "Welcome to EXORCIST.EXE: Case #1031 — The Murder of PID 1, an air-gapped cyber-noir digital forensics interrogation game built for Hacktoberfest 2026: 'Ghost in the Machine'. "
        "You play as Detective Ray Trace, an air-gapped Digital Coroner summoned to Sector 0x7FFF before the hardware watchdog timer triggers a catastrophic Kernel Panic."
    ),
    (
        26.0,
        "Four primary system daemons have been detained in the interrogation room: systemd, GarbageCollector, CronDaemon, and Daemon 666. "
        "Under the hood, EXORCIST.EXE is powered entirely by open-weight AI—running locally with Ollama using Gemma 2 and Llama 3.2, backed by a zero-dependency offline heuristic matrix. "
        "Zero cloud API keys. Zero user telemetry sent to corporate servers. 100% privacy and air-gapped local deduction."
    ),
    (
        51.0,
        "Let's inspect the evidence locker. In syslog, an unauthorized process bound a raw socket to port 666 seconds before the crash. "
        "And here's the smoking gun: in core.dump, PID 1's stack was smashed with 0x41, and the Instruction Pointer was hijacked to point to 0x7FFFDEADBEEF! "
        "Let's slam this evidence directly onto the interrogation table."
    ),
    (
        75.0,
        "Daemon 666 cracks under the weight of the evidence! "
        "Notice how the tension meter surges to 95%, triggering real-time visual glitch shaders and procedural Web Audio distortion synthesized purely in code. "
        "The Ghost confesses to injecting shellcode through raw port 666. The case is ready for trial."
    ),
    (
        96.0,
        "We open the indictment terminal. Accused: Daemon 666. "
        "Murder Weapon: Stack Buffer Overflow. Exorcism Command: kill -9 666. "
        "Execute! "
        "Verdict: GUILTY_EXORCISED! Score: 100 out of 100. "
        "The hardware watchdog timer halts, PID 1 reboots cleanly, and the mainframe is purified!"
    ),
    (
        113.0,
        "You can play EXORCIST.EXE right now in your browser with zero install on GitHub Pages, or inside your terminal via Python CLI. "
        "Open-source AI belongs on-device, offline, and in developers' hands. "
        "Don't let your code become a ghost in the machine. Happy Hacktoberfest!"
    )
]

def synthesize_elevenlabs(text: str, output_path: str, api_key: str, voice_name: str = "Adam") -> bool:
    try:
        from elevenlabs.client import ElevenLabs
        client = ElevenLabs(api_key=api_key)
        audio_generator = client.generate(
            text=text,
            voice=voice_name,
            model="eleven_multilingual_v2"
        )
        with open(output_path, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)
        return True
    except Exception as e:
        print(f"ElevenLabs synthesis warning ({e}), falling back to studio neural voice.", flush=True)
        return False

async def synthesize_neural(text: str, output_path: str, voice: str = "en-US-ChristopherNeural") -> None:
    import edge_tts
    communicate = edge_tts.Communicate(text=text, voice=voice, rate="+5%", pitch="-3Hz")
    await communicate.save(output_path)

async def build_audio_track(output_wav: str, api_key: str = None) -> None:
    temp_dir = os.path.join(os.path.dirname(__file__), "demo_recording", "temp_audio")
    os.makedirs(temp_dir, exist_ok=True)
    
    segment_files = []
    for i, (start_time, text) in enumerate(SCRIPT_SEGMENTS):
        seg_file = os.path.join(temp_dir, f"seg_{i}.mp3")
        success = False
        if api_key:
            print(f">> [Segment {i+1}/6] Synthesizing via ElevenLabs API (Voice: Adam)...", flush=True)
            success = synthesize_elevenlabs(text, seg_file, api_key)
        
        if not success:
            print(f">> [Segment {i+1}/6] Synthesizing via Studio Cyber-Noir Voice (Christopher)...", flush=True)
            await synthesize_neural(text, seg_file)
        
        segment_files.append((start_time, seg_file))

    # Assemble using ffmpeg adelay and amix
    print(">> Assembling synchronized audio track with FFmpeg...", flush=True)
    inputs = []
    filter_complex = []
    
    for i, (start_time, fpath) in enumerate(segment_files):
        inputs.extend(["-i", fpath])
        delay_ms = int(start_time * 1000)
        filter_complex.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}];")
    
    mix_inputs = "".join(f"[a{i}]" for i in range(len(segment_files)))
    filter_complex.append(f"{mix_inputs}amix=inputs={len(segment_files)}:dropout_transition=2:normalize=0[outa]")
    
    cmd = [
        FFMPEG_EXE, "-y",
        *inputs,
        "-filter_complex", "".join(filter_complex),
        "-map", "[outa]",
        "-ac", "2",
        "-ar", "44100",
        output_wav
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f">> Full narration track created: {output_wav}", flush=True)

def merge_video_audio(video_in: str, audio_in: str, video_out: str) -> None:
    print(f">> Merging video {video_in} with audio {audio_in} -> {video_out}...", flush=True)
    cmd = [
        FFMPEG_EXE, "-y",
        "-i", video_in,
        "-i", audio_in,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        video_out
    ]
    subprocess.run(cmd, check=True)
    print(f">> Final Demo Video Successfully Created: {video_out}", flush=True)

async def main():
    parser = argparse.ArgumentParser(description="Generate 2min Demo Video with ElevenLabs/Neural Audio")
    parser.add_argument("--api-key", default=os.getenv("ELEVENLABS_API_KEY"), help="ElevenLabs API Key")
    parser.add_argument("--voice", default="Adam", help="ElevenLabs Voice Name")
    args = parser.parse_args()

    demo_dir = os.path.join(os.path.dirname(__file__), "demo_recording")
    video_source = os.path.join(demo_dir, "exorcist_2min_demo.webm")
    narration_audio = os.path.join(demo_dir, "exorcist_narration.wav")
    final_mp4 = os.path.join(demo_dir, "exorcist_final_demo_with_audio.mp4")

    if not os.path.exists(video_source):
        print(f"Error: Base video {video_source} not found! Run record_demo.py first.")
        sys.exit(1)

    print("=" * 60, flush=True)
    print(">> EXORCIST.EXE // 2-MINUTE DEMO AUDIO COMPOSITOR", flush=True)
    print("=" * 60, flush=True)

    await build_audio_track(narration_audio, api_key=args.api_key)
    merge_video_audio(video_source, narration_audio, final_mp4)

    file_size_mb = os.path.getsize(final_mp4) / (1024 * 1024)
    print("=" * 60, flush=True)
    print(f">> SUCCESS! Final presentation video: {final_mp4} ({file_size_mb:.2f} MB)", flush=True)
    print("=" * 60, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
