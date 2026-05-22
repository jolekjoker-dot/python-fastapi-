import json
from pathlib import Path

from backend.schemas.quest import (
    QuestData,
    QuestSummary,
    QuestTask,
    TaskSubmit,
    TaskSubmitResult,
    TestResult,
)
from backend.services.code_executor import execute_raw


_quests_dir = Path(__file__).resolve().parent.parent / "data" / "quests"
_quest_cache: dict[str, QuestData] = {}


def _load_quest(quest_id: str) -> QuestData | None:
    if quest_id in _quest_cache:
        return _quest_cache[quest_id]

    path = _quests_dir / f"{quest_id}.json"
    if not path.exists():
        return None

    data = json.loads(path.read_text(encoding="utf-8"))
    quest = QuestData.model_validate(data)
    _quest_cache[quest_id] = quest
    return quest


def list_quests(completed_set: set[str]) -> list[QuestSummary]:
    quests: list[QuestSummary] = []
    json_files = sorted(_quests_dir.glob("quest_*.json"))

    prev_completed = True
    for f in json_files:
        quest = _load_quest(f.stem)
        if quest is None:
            continue
        completed = quest.id in completed_set
        quests.append(
            QuestSummary(
                id=quest.id,
                title=quest.title,
                phase=quest.phase,
                order=quest.order,
                xp_reward=quest.xp_reward,
                completed=completed,
                unlocked=prev_completed,
            )
        )
        prev_completed = completed

    return quests


def get_quest(quest_id: str) -> QuestData | None:
    return _load_quest(quest_id)


def check_task(quest_id: str, submit: TaskSubmit) -> TaskSubmitResult:
    quest = _load_quest(quest_id)
    if quest is None:
        return TaskSubmitResult(
            task_id=submit.task_id,
            passed=False,
            test_results=[],
            execution_time=0,
            stderr=f"Quest {quest_id} not found",
        )

    task: QuestTask | None = None
    for t in quest.tasks:
        if t.id == submit.task_id:
            task = t
            break
    if task is None and quest.challenge and quest.challenge.id == submit.task_id:
        task = quest.challenge
    if task is None:
        return TaskSubmitResult(
            task_id=submit.task_id,
            passed=False,
            test_results=[],
            execution_time=0,
            stderr=f"Task {submit.task_id} not found",
        )

    test_results: list[TestResult] = []
    all_passed = True
    total_time = 0.0
    combined_stdout = ""
    combined_stderr = ""

    # FastAPI HTTP tests — use special executor
    if task.test_cases and task.test_cases[0].type == "http_test":
        from backend.services.fastapi_executor import execute_fastapi

        http_cases = [
            {
                "method": tc.method,
                "path": tc.path,
                "expected_status": tc.expected_status,
                "expected_body_contains": tc.expected_body_contains,
                "body": tc.body,
                "description": tc.description,
            }
            for tc in task.test_cases
        ]
        result = execute_fastapi(submit.code, http_cases)
        total_time = result.get("execution_time", 0.0)
        all_passed = result.get("passed", False)
        stderr = result.get("error", "") or ""

        for tc in result.get("test_results", []):
            test_results.append(
                TestResult(
                    passed=tc.get("passed", False),
                    description=tc.get("description", ""),
                    expected=tc.get("expected", ""),
                    actual=tc.get("actual", ""),
                    error=tc.get("error"),
                )
            )

        return TaskSubmitResult(
            task_id=submit.task_id,
            passed=all_passed,
            test_results=test_results,
            execution_time=round(total_time, 4),
            stdout="",
            stderr=stderr,
        )

    # HTML frontend tests — serve via HTTP and check page source
    if task.test_cases and task.test_cases[0].type == "html_check":
        from backend.services.frontend_executor import execute_html

        html_cases = [
            {"expected_body_contains": tc.expected_body_contains, "description": tc.description}
            for tc in task.test_cases
        ]
        result = execute_html(submit.code, html_cases)
        total_time = result.get("execution_time", 0.0)
        all_passed = result.get("passed", False)
        stderr = result.get("error", "") or ""

        for tc in result.get("test_results", []):
            test_results.append(
                TestResult(
                    passed=tc.get("passed", False),
                    description=tc.get("description", ""),
                    expected=tc.get("expected", ""),
                    actual=tc.get("actual", ""),
                    error=tc.get("error"),
                )
            )

        return TaskSubmitResult(
            task_id=submit.task_id,
            passed=all_passed,
            test_results=test_results,
            execution_time=round(total_time, 4),
            stdout="",
            stderr=stderr,
        )

    for tc in task.test_cases:
        if tc.input_data is not None:
            wrapper = (
                f"import sys, io\n"
                f"sys.stdin = io.StringIO({json.dumps(tc.input_data)})\n"
                f"{submit.code}"
            )
        else:
            wrapper = submit.code

        result = execute_raw(wrapper)
        total_time += result.execution_time
        combined_stdout += result.stdout
        combined_stderr += result.stderr

        actual = result.stdout.strip()
        expected = tc.expected.strip()

        if tc.type == "output_contains":
            passed = expected in actual
        else:
            passed = actual == expected

        if not passed and result.stderr:
            passed = False

        test_results.append(
            TestResult(
                passed=passed,
                description=tc.description,
                expected=expected,
                actual=actual,
                error=result.stderr if result.stderr else None,
            )
        )

        if not passed:
            all_passed = False

    return TaskSubmitResult(
        task_id=submit.task_id,
        passed=all_passed,
        test_results=test_results,
        execution_time=round(total_time, 4),
        stdout=combined_stdout.strip(),
        stderr=combined_stderr.strip(),
    )
