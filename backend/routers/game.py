from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.execution import ExecutionHistory, UserPreference
from backend.models.progress import Progress
from backend.models.user import User
from backend.schemas.user import UserResponse
from backend.services.auth_service import get_current_user
from backend.services.game_service import (
    ACHIEVEMENTS,
    SHOP_ITEMS,
    check_achievements,
    get_or_create_preferences,
    get_user_stats,
)

router = APIRouter(prefix="/api/game", tags=["game"])


# ── achievements ──

@router.get("/achievements")
async def get_achievements(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    pref = await db.execute(
        select(UserPreference).where(
            UserPreference.user_id == current_user.id,
            UserPreference.key == "achievements",
        )
    )
    pref_row = pref.scalar_one_or_none()
    unlocked_ids = set(pref_row.value.split(",")) if pref_row and pref_row.value else set()

    return [
        {
            "id": a["id"],
            "name": a["name"],
            "icon": a["icon"],
            "desc": a["desc"],
            "unlocked": a["id"] in unlocked_ids,
            "xp": a["xp"],
        }
        for a in ACHIEVEMENTS
    ]


# ── check achievements after quest completion ──

@router.post("/check-achievements")
async def trigger_achievement_check(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stats = await get_user_stats(current_user, db)
    new_achievements = check_achievements(
        stats["completed_count"],
        stats["total_submits"],
        stats["all_quest_one_shot"],
        stats["best_time"],
    )

    pref_row = await db.execute(
        select(UserPreference).where(
            UserPreference.user_id == current_user.id,
            UserPreference.key == "achievements",
        )
    )
    pref = pref_row.scalar_one_or_none()
    current_ids = set(pref.value.split(",")) if pref and pref.value else set()

    newly_unlocked = []
    for a in new_achievements:
        if a["id"] not in current_ids:
            current_ids.add(a["id"])
            newly_unlocked.append(a)

    if newly_unlocked:
        if pref:
            pref.value = ",".join(sorted(current_ids))
        else:
            db.add(UserPreference(user_id=current_user.id, key="achievements", value=",".join(sorted(current_ids))))
        await db.commit()

    return {"new_achievements": newly_unlocked}


# ── checkin / streak ──

@router.post("/checkin")
async def checkin(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    today = str(date.today())
    pref_row = await db.execute(
        select(UserPreference).where(
            UserPreference.user_id == current_user.id,
            UserPreference.key == "checkins",
        )
    )
    pref = pref_row.scalar_one_or_none()
    checkins = set(pref.value.split(",")) if pref and pref.value else set()

    if today in checkins:
        streak = _calc_streak(checkins)
        return {"streak": streak, "already_checked": True}

    checkins.add(today)
    if pref:
        pref.value = ",".join(sorted(checkins))
    else:
        db.add(UserPreference(user_id=current_user.id, key="checkins", value=",".join(sorted(checkins))))
    await db.commit()

    streak = _calc_streak(checkins)
    return {"streak": streak, "already_checked": False}


def _calc_streak(checkins: set[str]) -> int:
    streak = 0
    d = date.today()
    while str(d) in checkins:
        streak += 1
        d -= __import__("datetime").timedelta(days=1)
    return streak


@router.get("/checkin")
async def get_checkin(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    pref_row = await db.execute(
        select(UserPreference).where(
            UserPreference.user_id == current_user.id,
            UserPreference.key == "checkins",
        )
    )
    pref = pref_row.scalar_one_or_none()
    checkins = set(pref.value.split(",")) if pref and pref.value else set()
    return {
        "checkins": sorted(checkins),
        "streak": _calc_streak(checkins),
    }


# ── shop ──

@router.get("/shop")
async def get_shop():
    return {"items": SHOP_ITEMS}


@router.post("/shop/buy/{item_id}")
async def buy_item(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    item = next((i for i in SHOP_ITEMS if i["id"] == item_id), None)
    if item is None:
        return {"ok": False, "error": "商品不存在"}

    # Check already owned
    prefs = await get_or_create_preferences(current_user.id, db)
    owned = prefs.get(f"shop_{item_id}", "")
    if owned == "1":
        return {"ok": False, "error": "已拥有此商品"}

    if current_user.coins < item["price"]:
        return {"ok": False, "error": f"金币不足（需要 {item['price']}，当前 {current_user.coins}）"}

    current_user.coins -= item["price"]

    existing = await db.execute(
        select(UserPreference).where(
            UserPreference.user_id == current_user.id,
            UserPreference.key == f"shop_{item_id}",
        )
    )
    p = existing.scalar_one_or_none()
    if p:
        p.value = "1"
    else:
        db.add(UserPreference(user_id=current_user.id, key=f"shop_{item_id}", value="1"))
    await db.commit()

    return {"ok": True, "coins": current_user.coins}


# ── leaderboard ──

@router.get("/leaderboard", response_model=list[UserResponse])
async def leaderboard(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).order_by(User.xp.desc()).limit(20)
    )
    return result.scalars().all()
