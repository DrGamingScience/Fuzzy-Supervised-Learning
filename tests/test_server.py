"""Nghiệm thu server local thật: khởi động, HTTP health/trang chủ và dừng."""

from pathlib import Path
import os
import socket
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener


def test_streamlit_starts_serves_and_stops(tmp_path):
    root = Path(__file__).resolve().parents[1]
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    url = f"http://127.0.0.1:{port}"
    # Không dùng HTTP proxy của máy cho phép kiểm tra loopback.
    opener = build_opener(ProxyHandler({}))
    log_path = tmp_path / "streamlit.log"
    with log_path.open("w", encoding="utf-8") as log:
        server = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "app.py",
             "--server.address=127.0.0.1", f"--server.port={port}",
             "--server.headless=true", "--browser.gatherUsageStats=false"],
            cwd=root, stdout=log, stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        try:
            deadline = time.monotonic() + 30
            while True:
                assert server.poll() is None, log_path.read_text(encoding="utf-8")
                try:
                    with opener.open(url + "/_stcore/health", timeout=1) as response:
                        assert response.status == 200
                        assert response.read() == b"ok"
                    break
                except (URLError, TimeoutError):
                    if time.monotonic() >= deadline:
                        raise AssertionError(log_path.read_text(encoding="utf-8"))
                    time.sleep(0.1)
            with opener.open(url, timeout=3) as response:
                assert response.status == 200
                assert b"<html" in response.read().lower()
        finally:
            server.terminate()
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=5)
        assert server.poll() is not None
    with socket.socket() as probe:
        probe.settimeout(1)
        assert probe.connect_ex(("127.0.0.1", port)) != 0, "Server vẫn còn nghe sau khi dừng"
