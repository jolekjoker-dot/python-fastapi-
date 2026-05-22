from fastapi import APIRouter, Depends, Query
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.execution import CodeDraft, ExecutionHistory, UserPreference
from backend.models.user import User
from backend.schemas.persistence import (
    CodeDraftResponse,
    CodeDraftSave,
    ExecutionRecord,
    PreferenceSave,
)
from backend.services.auth_service import get_current_user

router = APIRouter(prefix="/api", tags=["persistence"])


# ── execution history ──

@router.get("/history", response_model=list[ExecutionRecord])
async def get_history(
    quest_id: str | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(ExecutionHistory)
        .where(ExecutionHistory.user_id == current_user.id)
        .order_by(ExecutionHistory.created_at.desc())
        .limit(50)
    )
    if quest_id:
        stmt = stmt.where(ExecutionHistory.quest_id == quest_id)
    result = await db.execute(stmt)
    return result.scalars().all()


# ── code drafts ──

@router.get("/drafts/{quest_id}/{task_id}", response_model=CodeDraftResponse)
async def get_draft(
    quest_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(CodeDraft).where(
            CodeDraft.user_id == current_user.id,
            CodeDraft.quest_id == quest_id,
            CodeDraft.task_id == task_id,
        )
    )
    draft = result.scalar_one_or_none()
    if draft is None:
        return CodeDraftResponse(quest_id=quest_id, task_id=task_id, code="")
    return draft


@router.post("/drafts")
async def save_draft(
    data: CodeDraftSave,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(CodeDraft).where(
            CodeDraft.user_id == current_user.id,
            CodeDraft.quest_id == data.quest_id,
            CodeDraft.task_id == data.task_id,
        )
    )
    draft = result.scalar_one_or_none()
    if draft:
        draft.code = data.code
    else:
        draft = CodeDraft(
            user_id=current_user.id,
            quest_id=data.quest_id,
            task_id=data.task_id,
            code=data.code,
        )
        db.add(draft)
    await db.commit()
    return {"ok": True}


# ── user preferences ──

@router.get("/preferences")
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(UserPreference).where(UserPreference.user_id == current_user.id)
    )
    prefs = result.scalars().all()
    return {p.key: p.value for p in prefs}


@router.post("/preferences")
async def save_preference(
    data: PreferenceSave,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(UserPreference).where(
            UserPreference.user_id == current_user.id,
            UserPreference.key == data.key,
        )
    )
    pref = result.scalars().first()
    if pref:
        pref.value = data.value
    else:
        pref = UserPreference(user_id=current_user.id, key=data.key, value=data.value)
        db.add(pref)
    await db.commit()
    return {"ok": True}
