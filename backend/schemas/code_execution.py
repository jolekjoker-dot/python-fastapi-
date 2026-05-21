from pydantic import BaseModel


class CodeSubmit(BaseModel):
    code: str


class ExecutionResult(BaseModel):
    stdout: str
    stderr: str
    passed: bool
    execution_time: float
    error: str | None = None
