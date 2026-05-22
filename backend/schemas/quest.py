from pydantic import BaseModel


class TestCase(BaseModel):
    type: str = "output_match"
    expected: str
    input_data: str | None = None
    description: str = ""


class QuestTask(BaseModel):
    id: str
    description: str
    starter_code: str
    test_cases: list[TestCase]
    hints: list[str] = []
    order: int = 1


class QuestData(BaseModel):
    id: str
    title: str
    phase: int
    order: int
    story: str
    content: str
    tasks: list[QuestTask]
    challenge: QuestTask | None = None
    xp_reward: int = 100
    coin_reward: int = 50


class QuestSummary(BaseModel):
    id: str
    title: str
    phase: int
    order: int
    xp_reward: int
    completed: bool = False
    unlocked: bool = False


class TaskSubmit(BaseModel):
    task_id: str
    code: str


class TestResult(BaseModel):
    passed: bool
    description: str
    expected: str
    actual: str
    error: str | None = None


class TaskSubmitResult(BaseModel):
    task_id: str
    passed: bool
    test_results: list[TestResult]
    execution_time: float
    stdout: str = ""
    stderr: str = ""


class QuestProgress(BaseModel):
    quest_id: str
    completed: bool
    completed_tasks: list[str]
