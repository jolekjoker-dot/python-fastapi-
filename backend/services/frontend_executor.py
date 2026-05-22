import subprocess
import tempfile
import time
from pathlib import Path

import httpx

from backend.sandbox.security import SecurityError, check_code


def execute_html(code: str, test_cases: list[dict]) -> dict:
    """Serve user HTML via a temp HTTP server and run checks against the page source."""

    try:
        check_code(code)
    except SecurityError as e:
        return {"passed": False, "error": str(e), "test_results": []}

    # Find a free port
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    tmp_dir = Path(tempfile.gettempdir()) / f"code_quest_html_{hash(code) & 0x7FFFFFFF}"
    tmp_dir.mkdir(exist_ok=True)
    html_file = tmp_dir / "index.html"
    html_file.write_text(code, encoding="utf-8")

    proc = None
    try:
        proc = subprocess.Popen(
            ["python", "-m", "http.server", str(port)],
            cwd=str(tmp_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        base_url = f"http://127.0.0.1:{port}"
        ready = False
        for _ in range(15):
            time.sleep(0.2)
            try:
                r = httpx.get(base_url, timeout=1)
                if r.status_code == 200:
                    ready = True
                    break
            except Exception:
                continue

        if not ready:
            return {
                "passed": False,
                "error": "HTTP 服务器启动失败",
                "test_results": [],
                "execution_time": 3.0,
            }

        test_results = []
        all_passed = True
        total_time = 0.0

        for tc in test_cases:
            start = time.perf_counter()
            try:
                resp = httpx.get(base_url, timeout=3)
                elapsed = time.perf_counter() - start
                total_time += elapsed

                source = resp.text
                expected_contains = tc.get("expected_body_contains", "")
                description = tc.get("description", "")

                passed = expected_contains in source if expected_contains else True
                if not passed:
                    all_passed = False

                test_results.append({
                    "passed": passed,
                    "description": description,
                    "expected": expected_contains[:100] if expected_contains else "(any)",
                    "actual": source[:200] if not passed else expected_contains[:100],
                    "error": None,
                })
            except Exception as e:
                all_passed = False
                test_results.append({
                    "passed": False,
                    "description": tc.get("description", ""),
                    "expected": tc.get("expected_body_contains", "")[:100],
                    "actual": str(e),
                    "error": str(e),
                })

        return {
            "passed": all_passed,
            "error": None,
            "test_results": test_results,
            "execution_time": round(total_time, 3),
        }

    finally:
        if proc:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
        if html_file.exists():
            html_file.unlink()
        try:
            tmp_dir.rmdir()
        except OSError:
            pass
