import os
import sys
import time
from playwright.sync_api import sync_playwright

def record_exorcist_demo():
    output_dir = os.path.join(os.path.dirname(__file__), "demo_recording")
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print(">> EXORCIST.EXE // AUTOMATED CINEMATIC DEMO RECORDER")
    print(f">> Output Directory: {output_dir}")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir=output_dir,
            record_video_size={"width": 1920, "height": 1080},
            viewport={"width": 1920, "height": 1080}
        )

        page = context.new_page()

        # Step 1: Navigate to Live Deployment
        print("[0:00 - 0:15] Booting Crime Lab HUD...")
        page.goto("https://tribhu05.github.io/exorcist-exe/", wait_until="networkidle")
        page.wait_for_timeout(4000)

        # Step 2: Hover and inspect briefing strip
        print("[0:15 - 0:30] Surveying Crime Scene & Dossier...")
        page.mouse.move(300, 200)
        page.wait_for_timeout(2000)
        page.mouse.move(960, 200)
        page.wait_for_timeout(2000)

        # Step 3: Browse Suspect Daemons
        print("[0:30 - 0:50] Inspecting Detained Suspect Daemons...")
        suspect_buttons = page.locator("button:has-text('systemd'), button:has-text('GarbageCollector'), button:has-text('CronDaemon'), button:has-text('Daemon 666')")
        
        # Click systemd
        page.click("text=systemd (PID 1 Supervisor)")
        page.wait_for_timeout(2500)

        # Click GarbageCollector
        page.click("text=GarbageCollector (GC)")
        page.wait_for_timeout(2500)

        # Click CronDaemon
        page.click("text=CronDaemon (crond)")
        page.wait_for_timeout(2500)

        # Click Daemon 666
        page.click("text=Daemon 666 (The Phantom Socket)")
        page.wait_for_timeout(3000)

        # Step 4: Inspect Evidence Locker
        print("[0:50 - 1:10] Inspecting Forensic Evidence Locker...")
        # Scroll down to Evidence section
        page.evaluate("window.scrollBy({ top: 400, behavior: 'smooth' })")
        page.wait_for_timeout(2000)

        # View Syslog
        page.click("text=Corrupted Syslog (/var/log/syslog)")
        page.wait_for_timeout(3000)

        # View Core Dump
        page.click("text=Stack Memory Hex Dump (core.dump)")
        page.wait_for_timeout(3000)

        # Click Confront Suspect with this Evidence button if visible
        confront_btn = page.locator("button:has-text('CONFRONT SUSPECT WITH THIS EVIDENCE')")
        if confront_btn.is_visible():
            confront_btn.click()
            page.wait_for_timeout(2000)

        # Step 5: Interrogation Room
        print("[1:10 - 1:35] Confronting Daemon 666 in Interrogation Room...")
        page.evaluate("window.scrollTo({ top: 350, behavior: 'smooth' })")
        page.wait_for_timeout(1500)

        # Type question with human typing speed
        input_box = page.locator("input[placeholder*='Question'], input[placeholder*='Ask'], input[type='text']")
        if input_box.is_visible():
            input_box.click()
            question = "Explain the 0xDEADBEEF signature in this core dump!"
            for char in question:
                page.keyboard.type(char, delay=35)
                time.sleep(0.01)
            page.wait_for_timeout(1000)
            page.keyboard.press("Enter")
            print(">> Sent confrontation message! Waiting for Daemon 666 tension reaction...")
            page.wait_for_timeout(7000)

        # Step 6: Execute Exorcism Indictment
        print("[1:35 - 1:55] Executing Terminal Exorcism Indictment...")
        # Scroll to top to see Navbar
        page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        page.wait_for_timeout(1500)

        page.click("button:has-text('EXECUTE EXORCISM')")
        page.wait_for_timeout(2000)

        # Select suspect radio in modal
        phantom_radio = page.locator("input[value='phantom_socket'], label:has-text('Daemon 666')")
        if phantom_radio.is_visible():
            phantom_radio.click()
            page.wait_for_timeout(1000)

        # Fill murder weapon input
        weapon_input = page.locator("input[placeholder*='Buffer'], input[placeholder*='overflow'], input[placeholder*='exploit']").first
        if weapon_input.is_visible():
            weapon_input.click()
            for char in "Stack Buffer Overflow / Smashing with 0xDEADBEEF":
                page.keyboard.type(char, delay=30)
            page.wait_for_timeout(1000)

        # Fill command input
        cmd_input = page.locator("input[placeholder*='kill'], input[placeholder*='command'], input[placeholder*='sysctl']").first
        if cmd_input.is_visible():
            cmd_input.click()
            for char in "kill -9 666":
                page.keyboard.type(char, delay=40)
            page.wait_for_timeout(1000)

        # Click Execute Exorcism button in modal
        exec_btn = page.locator("button:has-text('EXECUTE TERMINAL EXORCISM')")
        if exec_btn.is_visible():
            exec_btn.click()
            print(">> Exorcism Executed! Capturing verdict screen...")
            page.wait_for_timeout(8000)

        # Step 7: Outro hold
        print("[1:55 - 2:00] Final Scene Hold...")
        page.wait_for_timeout(5000)

        # Close page and context to finalize video
        page.close()
        video_path = page.video.path() if page.video else None
        context.close()
        browser.close()

    print("=" * 60)
    print(f">> DEMO RECORDING COMPLETE!")
    if video_path and os.path.exists(video_path):
        final_mp4 = os.path.join(output_dir, "exorcist_2min_demo.webm")
        if os.path.exists(final_mp4):
            os.remove(final_mp4)
        os.rename(video_path, final_mp4)
        print(f">> Saved high-definition demo video to: {final_mp4}")
    print("=" * 60)

if __name__ == "__main__":
    record_exorcist_demo()
