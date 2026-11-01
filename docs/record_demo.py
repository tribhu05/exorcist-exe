import os
import sys
import time
from playwright.sync_api import sync_playwright

def record_exorcist_demo():
    output_dir = os.path.join(os.path.dirname(__file__), "demo_recording")
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60, flush=True)
    print(">> EXORCIST.EXE // 2-MINUTE CINEMATIC DEMO RECORDER", flush=True)
    print(f">> Output Directory: {output_dir}", flush=True)
    print("=" * 60, flush=True)

    with sync_playwright() as p:
        print(">> Launching Chromium browser...", flush=True)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir=output_dir,
            record_video_size={"width": 1920, "height": 1080},
            viewport={"width": 1920, "height": 1080}
        )

        page = context.new_page()

        # Scene 1: Booting Crime Lab HUD & Case Briefing (0:00 - 0:25)
        print("[0:00 - 0:25] Scene 1: Booting Crime Lab HUD & Case Dossier...", flush=True)
        page.goto("https://tribhu05.github.io/exorcist-exe/", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(6000)
        page.mouse.move(350, 140)
        page.wait_for_timeout(4000)
        page.mouse.move(700, 140)
        page.wait_for_timeout(4000)
        page.mouse.move(1050, 140)
        page.wait_for_timeout(7000)

        # Scene 2: Surveying 4 Detained Suspect Daemons (0:25 - 0:50)
        print("[0:25 - 0:50] Scene 2: Surveying Suspect Daemons in Custody...", flush=True)
        try:
            page.locator("text=systemd").first.click(timeout=5000)
            page.wait_for_timeout(5500)
            page.locator("text=GarbageCollector").first.click(timeout=5000)
            page.wait_for_timeout(5500)
            page.locator("text=CronDaemon").first.click(timeout=5000)
            page.wait_for_timeout(5500)
            page.locator("text=Daemon 666").first.click(timeout=5000)
            page.wait_for_timeout(7000)
        except Exception as e:
            print(f"Warning during suspect browse: {e}", flush=True)

        # Scene 3: Inspecting Forensic Evidence Locker (0:50 - 1:15)
        print("[0:50 - 1:15] Scene 3: Inspecting Evidence Locker (Syslog & Core Dump)...", flush=True)
        page.evaluate("window.scrollBy({ top: 380, behavior: 'smooth' })")
        page.wait_for_timeout(2500)

        try:
            # View Corrupted Syslog
            page.locator("button:has-text('Corrupted Syslog')").first.click(timeout=5000)
            page.wait_for_timeout(7000)

            # View Core Dump
            page.locator("button:has-text('Stack Memory Hex Dump')").first.click(timeout=5000)
            page.wait_for_timeout(7000)

            # Click Confront with Clue button
            confront_btn = page.locator("button:has-text('WITH THIS CLUE')").first
            if confront_btn.is_visible():
                confront_btn.click()
                print(">> Confronted Daemon 666 with core.dump clue!", flush=True)
                page.wait_for_timeout(6000)
        except Exception as e:
            print(f"Warning during evidence locker: {e}", flush=True)

        # Scene 4: Interrogation Room Confrontation & Glitch Tension (1:15 - 1:35)
        print("[1:15 - 1:35] Scene 4: Interrogation Confrontation & Glitch Surge...", flush=True)
        page.evaluate("window.scrollTo({ top: 120, behavior: 'smooth' })")
        page.wait_for_timeout(2000)

        try:
            input_box = page.locator("input[placeholder*='Question'], input[placeholder*='interrogate'], input[type='text']").first
            if input_box.is_visible():
                input_box.click()
                question = "Explain the 0xDEADBEEF signature in this core dump!"
                for char in question:
                    page.keyboard.type(char, delay=30)
                page.wait_for_timeout(800)
                page.keyboard.press("Enter")
                print(">> Sent confrontation message! Watching tension surge to 95%...", flush=True)
                page.wait_for_timeout(16000)
        except Exception as e:
            print(f"Warning during interrogation: {e}", flush=True)

        # Scene 5: Terminal Exorcism Indictment & Verdict (1:35 - 1:52)
        print("[1:35 - 1:52] Scene 5: Executing Terminal Exorcism Indictment...", flush=True)
        page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        page.wait_for_timeout(1500)

        try:
            # Click Navbar Exorcise & Indict button
            page.locator("button:has-text('EXORCISE & INDICT')").click(timeout=5000)
            page.wait_for_timeout(2500)

            # Click Daemon 666 suspect button inside modal
            daemon_btn = page.locator("div[role='dialog'] button:has-text('Daemon 666'), .fixed button:has-text('Daemon 666')").first
            if daemon_btn.is_visible():
                daemon_btn.click()
                page.wait_for_timeout(2500)

            # Select preset kill -9 666
            preset_btn = page.locator("button:has-text('kill -9 666')").first
            if preset_btn.is_visible():
                preset_btn.click()
            else:
                cmd_input = page.locator("input[placeholder*='kill']").first
                if cmd_input.is_visible():
                    cmd_input.click()
                    cmd_input.fill("kill -9 666")
            page.wait_for_timeout(2000)

            # Click Execute button in modal
            exec_btn = page.locator("button:has-text('EXECUTE EXORCISM INDICTMENT')").first
            if exec_btn.is_visible():
                exec_btn.click()
                print(">> Exorcism Executed! Capturing verdict screen...", flush=True)
                page.wait_for_timeout(7000)
        except Exception as e:
            print(f"Warning during indictment: {e}", flush=True)

        # Scene 6: Victory Screen & Outro (1:52 - 2:12)
        print("[1:52 - 2:12] Scene 6: Victory Screen Hold & Hacktoberfest Outro...", flush=True)
        page.wait_for_timeout(20000)

        # Finalize video recording
        video_obj = page.video
        page.close()
        video_path = video_obj.path() if video_obj else None
        context.close()
        browser.close()

    print("=" * 60, flush=True)
    print(">> DEMO RECORDING COMPLETE!", flush=True)
    if video_path and os.path.exists(video_path):
        final_mp4 = os.path.join(output_dir, "exorcist_2min_demo.webm")
        if os.path.exists(final_mp4):
            os.remove(final_mp4)
        os.rename(video_path, final_mp4)
        file_size_mb = os.path.getsize(final_mp4) / (1024 * 1024)
        print(f">> Saved calibrated 2-minute demo video to: {final_mp4} ({file_size_mb:.2f} MB)", flush=True)
    print("=" * 60, flush=True)

if __name__ == "__main__":
    record_exorcist_demo()
