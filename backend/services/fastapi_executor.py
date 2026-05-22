import subprocess
import tempfile
import time
from pathlib import Path

import httpx

from backend.config import settings
from backend.sandbox.security import SecurityError, check_code


def execute_fastapi(code: str, test_cases: list[dict]) -> dict:
    """Start a temp FastAPI server, run HTTP test cases, return results."""

    try:
        check_code(code)
    except SecurityError as e:
        return {
            "passed": False,
            "error": str(e),
            "test_results": [],
        }

    # Find a free port
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    tmp_dir = Path(tempfile.gettempdir()) / f"code_quest_fastapi_{hash(code) & 0x7FFFFFFF}"
    tmp_dir.mkdir(exist_ok=True)
    main_file = tmp_dir / "main.py"
    main_file.write_text(code, encoding="utf-8")

    proc = None
    try:
        proc = subprocess.Popen(
            [settings.PYTHON_PATH, "-m", "uvicorn", "main:app", "--port", str(port), "--host", "127.0.0.1"],
            cwd=str(tmp_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Wait for server to be ready (poll up to 5 seconds)
        base_url = f"http://127.0.0.1:{port}"
        ready = False
        for _ in range(25):
            time.sleep(0.2)
            try:
                r = httpx.get(f"{base_url}/openapi.json", timeout=1)
                if r.status_code == 200:
                    ready = True
                    break
            except Exception:
                continue

        if not ready:
            return {
                "passed": False,
                "error": "服务器启动失败，请检查代码是否正确（需要创建名为 app 的 FastAPI 实例）",
                "test_results": [],
                "execution_time": 5.0,
            }

        # Run test cases
        test_results = []
        all_passed = True
        total_time = 0.0

        for tc in test_cases:
            method = tc.get("method", "GET").upper()
            path = tc["path"]
            expected_status = tc.get("expected_status", 200)
            expected_contains = tc.get("expected_body_contains", None)
            description = tc.get("description", "")

            start = time.perf_counter()
            try:
                if method == "GET":
                    resp = httpx.get(f"{base_url}{path}", timeout=5)
                elif method == "POST":
                    body = tc.get("body", {})
                    resp = httpx.post(f"{base_url}{path}", json=body, timeout=5)
                elif method == "PUT":
                    body = tc.get("body", {})
                    resp = httpx.put(f"{base_url}{path}", json=body, timeout=5)
                elif method == "DELETE":
                    resp = httpx.delete(f"{base_url}{path}", timeout=5)
                else:
                    resp = httpx.get(f"{base_url}{path}", timeout=5)

                elapsed = time.perf_counter() - start
                total_time += elapsed

                status_ok = resp.status_code == expected_status
                body_text = resp.text

                if expected_contains:
                    body_ok = expected_contains in body_text
                else:
                    body_ok = True

                passed = status_ok and body_ok
                if not passed:
                    all_passed = False

                detail = ""
                if not status_ok:
                    detail = f"期望状态码 {expected_status}，实际 {resp.status_code}"
                elif not body_ok:
                    detail = f"响应体中未找到 \"{expected_contains}\""

                test_results.append({
                    "passed": passed,
                    "description": description,
                    "expected": f"Status {expected_status}" + (f" + '{expected_contains}'" if expected_contains else ""),
                    "actual": f"Status {resp.status_code}" + (f" + '{body_text[:100]}'" if not body_ok else ""),
                    "detail": detail,
                    "error": None,
                })
            except Exception as e:
                all_passed = False
                test_results.append({
                    "passed": False,
                    "description": description,
                    "expected": f"Status {expected_status}",
                    "actual": f"请求失败: {e}",
                    "detail": str(e),
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
        # Cleanup
        if main_file.exists():
            main_file.unlink()
        try:
            tmp_dir.rmdir()
        except OSError:
            pass
