import os
import time
from playwright.sync_api import sync_playwright

def capture_screenshots():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
    os.makedirs(out_dir, exist_ok=True)
    
    print(f">> Capturing high-resolution screenshots to: {out_dir}", flush=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1
        )
        page = context.new_page()

        # 1. Main Crime Lab HUD
        print(">> Navigating to live deployment...", flush=True)
        page.goto("https://tribhu05.github.io/exorcist-exe/", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(4000)

        p1 = os.path.join(out_dir, "01_crime_lab_hud.png")
        page.screenshot(path=p1, full_page=False)
        print(f"Captured: {p1}", flush=True)

        # 2. Select suspect and interrogate
        try:
            page.locator("text=Daemon 666").first.click(timeout=5000)
            page.wait_for_timeout(2000)
            p2 = os.path.join(out_dir, "02_suspect_interrogation.png")
            page.screenshot(path=p2, full_page=False)
            print(f"Captured: {p2}", flush=True)
        except Exception as e:
            print(f"Warning on suspect click: {e}", flush=True)

        # 3. Evidence Locker - Core Dump
        try:
            page.evaluate("window.scrollBy({ top: 350, behavior: 'smooth' })")
            page.wait_for_timeout(1500)
            page.locator("button:has-text('Stack Memory Hex Dump')").first.click(timeout=5000)
            page.wait_for_timeout(2000)
            p3 = os.path.join(out_dir, "03_forensic_evidence_locker.png")
            page.screenshot(path=p3, full_page=False)
            print(f"Captured: {p3}", flush=True)

            # Confront Daemon 666 with clue
            confront_btn = page.locator("button:has-text('WITH THIS CLUE')").first
            if confront_btn.is_visible():
                confront_btn.click()
                print(">> Confronted with clue!", flush=True)
                page.wait_for_timeout(2500)

            # Send a confrontation question to spike tension
            page.evaluate("window.scrollTo({ top: 100, behavior: 'smooth' })")
            page.wait_for_timeout(1500)
            input_box = page.locator("input[placeholder*='Question'], input[placeholder*='interrogate'], input[type='text']").first
            if input_box.is_visible():
                input_box.click()
                input_box.fill("Explain the 0xDEADBEEF buffer overflow signature in this core dump!")
                page.keyboard.press("Enter")
                page.wait_for_timeout(5000)

            p4 = os.path.join(out_dir, "04_evidence_confrontation_glitch.png")
            page.screenshot(path=p4, full_page=False)
            print(f"Captured: {p4}", flush=True)

        except Exception as e:
            print(f"Warning on evidence locker: {e}", flush=True)

        # 5. Terminal Exorcism Modal & Verdict
        try:
            page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
            page.wait_for_timeout(1000)
            page.locator("button:has-text('EXORCISE & INDICT')").click(timeout=5000)
            page.wait_for_timeout(2000)

            daemon_btn = page.locator("div[role='dialog'] button:has-text('Daemon 666'), .fixed button:has-text('Daemon 666')").first
            if daemon_btn.is_visible():
                daemon_btn.click()
                page.wait_for_timeout(1000)

            preset_btn = page.locator("button:has-text('kill -9 666')").first
            if preset_btn.is_visible():
                preset_btn.click()

            exec_btn = page.locator("button:has-text('EXECUTE EXORCISM INDICTMENT')").first
            if exec_btn.is_visible():
                exec_btn.click()
                page.wait_for_timeout(5000)

            p5 = os.path.join(out_dir, "05_terminal_exorcism_verdict.png")
            page.screenshot(path=p5, full_page=False)
            print(f"Captured: {p5}", flush=True)
        except Exception as e:
            print(f"Warning on exorcism verdict: {e}", flush=True)

        browser.close()
        print(">> All screenshots captured successfully!", flush=True)

if __name__ == "__main__":
    capture_screenshots()
