from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from backend.database import get_db
from backend.models.execution import ExecutionHistory
from backend.models.progress import Progress
from backend.models.user import User
from backend.schemas.quest import (
    QuestData,
    QuestSummary,
    TaskSubmit,
    TaskSubmitResult,
)
from backend.services.auth_service import get_current_user
from backend.services.quest_service import check_task, get_quest, list_quests

router = APIRouter(prefix="/api/quests", tags=["quests"])


@router.get("", response_model=list[QuestSummary])
async def get_quests(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Progress).where(
            Progress.user_id == current_user.id, Progress.completed.is_(True)
        )
    )
    completed = {p.quest_id for p in result.scalars().all()}
    return list_quests(completed)


@router.get("/{quest_id}", response_model=QuestData)
async def get_quest_detail(
    quest_id: str,
    current_user: User = Depends(get_current_user),
):
    quest = get_quest(quest_id)
    if quest is None:
        raise HTTPException(status_code=404, detail="关卡不存在")
    return quest


@router.post("/{quest_id}/submit", response_model=TaskSubmitResult)
async def submit_task(
    quest_id: str,
    submit: TaskSubmit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = check_task(quest_id, submit)

    # Save execution history
    hist = ExecutionHistory(
        user_id=current_user.id,
        quest_id=quest_id,
        task_id=submit.task_id,
        code=submit.code,
        stdout=result.stdout,
        stderr=result.stderr,
        passed=result.passed,
        execution_time=result.execution_time,
    )
    db.add(hist)

    if result.passed:
        result2 = await db.execute(
            select(Progress).where(
                Progress.user_id == current_user.id,
                Progress.quest_id == quest_id,
            )
        )
        progress = result2.scalar_one_or_none()
        if progress is None:
            progress = Progress(user_id=current_user.id, quest_id=quest_id)
            db.add(progress)

        progress.add_completed_task(submit.task_id)

        quest = get_quest(quest_id)
        if quest:
            total_tasks = len(quest.tasks) + (1 if quest.challenge else 0)
            if not progress.completed and len(progress.completed_task_list) >= total_tasks:
                progress.completed = True
                progress.completed_at = func.now()
                current_user.xp += quest.xp_reward
                current_user.coins += quest.coin_reward

        await db.commit()

    return result
