from fastapi import APIRouter
from backend.services.code_executor import execute
from backend.schemas.code_execution import CodeSubmit, ExecutionResult

router = APIRouter(prefix="/api", tags=["execute"])


@router.post("/execute", response_model=ExecutionResult)
async def execute_code(submit: CodeSubmit):
    return execute(submit.code)
