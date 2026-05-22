import subprocess
import tempfile
import time
from pathlib import Path

from backend.config import settings
from backend.sandbox.security import SecurityError, check_code
from backend.schemas.code_execution import ExecutionResult


def execute(code: str) -> ExecutionResult:
    """Execute Python code in a sandboxed subprocess and return the result."""

    try:
        check_code(code)
    except SecurityError as e:
        return ExecutionResult(
            stdout="",
            stderr=str(e),
            passed=False,
            execution_time=0.0,
            error=str(e),
        )

    return execute_raw(code)


def execute_raw(code: str) -> ExecutionResult:

    tmp_path = Path(tempfile.gettempdir()) / f"code_quest_{hash(code) & 0x7FFFFFFF}.py"
    tmp_path.write_text(code, encoding="utf-8")

    try:
        start = time.perf_counter()
        proc = subprocess.run(
            [settings.PYTHON_PATH, "-I", str(tmp_path)],
            capture_output=True,
            text=True,
            timeout=settings.SANDBOX_TIMEOUT,
            env={},
        )
        elapsed = time.perf_counter() - start

        return ExecutionResult(
            stdout=proc.stdout,
            stderr=proc.stderr,
            passed=proc.returncode == 0 and not proc.stderr,
            execution_time=round(elapsed, 4),
            error=None,
        )
    except subprocess.TimeoutExpired:
        return ExecutionResult(
            stdout="",
            stderr="代码执行超时（5秒限制）",
            passed=False,
            execution_time=settings.SANDBOX_TIMEOUT,
            error="执行超时",
        )
    finally:
        if tmp_path.exists():
            tmp_path.unlink()
