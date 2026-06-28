from __future__ import annotations

import argparse
import http.server
import shutil
import socketserver
import subprocess
import threading
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "portfolio-web"
ASSET_DIR = ROOT / "docs" / "assets"
SCREENSHOT_DIR = ASSET_DIR / "screenshots"
DEMO_DIR = ASSET_DIR / "demo"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


def serve_static(port: int) -> socketserver.TCPServer:
    handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(WEB_DIR), **kwargs)
    server = socketserver.TCPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def capture(port: int) -> None:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    frame_dir = DEMO_DIR / "frames"
    if frame_dir.exists():
        shutil.rmtree(frame_dir)
    frame_dir.mkdir(parents=True)

    url = f"http://127.0.0.1:{port}/"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1050}, device_scale_factor=1)
        page.goto(url, wait_until="networkidle")
        page.screenshot(path=ASSET_DIR / "cover.png", full_page=False)
        page.screenshot(path=SCREENSHOT_DIR / "01-dashboard.png", full_page=False)

        page.click("[data-scenario='safety']")
        page.wait_for_timeout(350)
        page.screenshot(path=SCREENSHOT_DIR / "02-safety-gate.png", full_page=False)

        page.click("[data-scenario='rag']")
        page.wait_for_timeout(350)
        page.screenshot(path=SCREENSHOT_DIR / "03-rollback-gate.png", full_page=False)

        page.evaluate("window.scrollTo(0, document.querySelector('#architecture').offsetTop)")
        page.wait_for_timeout(350)
        page.screenshot(path=SCREENSHOT_DIR / "04-architecture.png", full_page=False)

        page.evaluate("window.scrollTo(0, document.querySelector('#evidence').offsetTop)")
        page.wait_for_timeout(350)
        page.screenshot(path=SCREENSHOT_DIR / "05-evidence.png", full_page=False)

        for index, scenario in enumerate(["support", "safety", "rag", "support", "safety", "rag"], start=1):
            page.evaluate("window.scrollTo(0, 0)")
            page.click(f"[data-scenario='{scenario}']")
            page.wait_for_timeout(250)
            page.screenshot(path=frame_dir / f"frame-{index:03d}.png", full_page=False)
        browser.close()

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            "1",
            "-i",
            str(frame_dir / "frame-%03d.png"),
            "-c:v",
            "libvpx-vp9",
            "-pix_fmt",
            "yuv420p",
            "-b:v",
            "0",
            "-crf",
            "34",
            str(DEMO_DIR / "guided-demo.webm"),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture portfolio demo screenshots and WebM.")
    parser.add_argument("--port", type=int, default=4177)
    args = parser.parse_args()

    server = serve_static(args.port)
    try:
        time.sleep(0.4)
        capture(args.port)
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
