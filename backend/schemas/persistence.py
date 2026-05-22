from datetime import datetime

from pydantic import BaseModel


class ExecutionRecord(BaseModel):
    id: int
    quest_id: str
    task_id: str
    code: str
    stdout: str
    stderr: str
    passed: bool
    execution_time: float
    created_at: datetime

    model_config = {"from_attributes": True}


class CodeDraftSave(BaseModel):
    quest_id: str
    task_id: str
    code: str


class CodeDraftResponse(BaseModel):
    quest_id: str
    task_id: str
    code: str


class PreferenceSave(BaseModel):
    key: str
    value: str
