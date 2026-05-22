from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.execution import UserPreference
from backend.models.progress import Progress
from backend.models.user import User

# Achievement definitions
ACHIEVEMENTS = [
    {"id": "first_quest", "name": "初出茅庐", "icon": "🥚", "desc": "完成第 1 关", "xp": 50},
    {"id": "five_quests", "name": "见习法师", "icon": "📖", "desc": "完成 5 关", "xp": 100},
    {"id": "ten_quests", "name": "学霸之证", "icon": "📚", "desc": "完成 10 关（第一篇章）", "xp": 200},
    {"id": "python_master", "name": "Python 大师", "icon": "🐍", "desc": "完成全部 10 关 Python 基础", "xp": 300},
    {"id": "fastapi_master", "name": "魔法阵构筑者", "icon": "🏰", "desc": "完成全部 8 关 FastAPI", "xp": 400},
    {"id": "fullstack_master", "name": "全栈大法师", "icon": "👑", "desc": "完成全部 25 关", "xp": 1000},
    {"id": "speed_demon", "name": "闪电施法", "icon": "⚡", "desc": "单关用时 < 5 秒", "xp": 80},
    {"id": "perfect_quest", "name": "百发百中", "icon": "🎯", "desc": "一关内所有任务一次通过", "xp": 100},
    {"id": "ten_submits", "name": "勤学苦练", "icon": "💪", "desc": "累计提交 10 次代码", "xp": 60},
    {"id": "fifty_submits", "name": "代码工匠", "icon": "🔨", "desc": "累计提交 50 次代码", "xp": 150},
]

SHOP_ITEMS = [
    {"id": "extra_hint", "name": "额外提示", "icon": "💡", "price": 50, "desc": "获得更详细的解题提示"},
    {"id": "dark_theme", "name": "暗夜主题", "icon": "🌙", "price": 300, "desc": "解锁暗夜模式皮肤"},
    {"id": "gold_name", "name": "金色称号", "icon": "✨", "price": 500, "desc": "用户名添加金色光效"},
    {"id": "skip_card", "name": "跳过券", "icon": "⏭️", "price": 200, "desc": "跳过一个关卡（每篇章限 1 次）"},
]


def _get_achievement_ids(user_achievements: str) -> set[str]:
    return set(user_achievements.split(",")) if user_achievements else set()


def check_achievements(
    completed_count: int,
    total_submits: int,
    all_quest_one_shot: bool,
    best_time: float | None,
) -> list[dict]:
    """Return newly unlocked achievements based on current stats."""
    unlocked: list[dict] = []

    if completed_count >= 1:
        unlocked.append(ACHIEVEMENTS[0])  # first_quest
    if completed_count >= 5:
        unlocked.append(ACHIEVEMENTS[1])  # five_quests
    if completed_count >= 10:
        unlocked.append(ACHIEVEMENTS[2])  # ten_quests
    if completed_count >= 10:
        unlocked.append(ACHIEVEMENTS[3])  # python_master (simplified)
    if completed_count >= 18:
        unlocked.append(ACHIEVEMENTS[4])  # fastapi_master
    if completed_count >= 25:
        unlocked.append(ACHIEVEMENTS[5])  # fullstack_master
    if best_time is not None and best_time < 5.0:
        unlocked.append(ACHIEVEMENTS[6])  # speed_demon
    if all_quest_one_shot:
        unlocked.append(ACHIEVEMENTS[7])  # perfect_quest
    if total_submits >= 10:
        unlocked.append(ACHIEVEMENTS[8])  # ten_submits
    if total_submits >= 50:
        unlocked.append(ACHIEVEMENTS[9])  # fifty_submits

    return unlocked


async def get_user_stats(user: User, db: AsyncSession) -> dict:
    """Collect all user stats for achievement detection."""
    result = await db.execute(
        select(Progress).where(
            Progress.user_id == user.id, Progress.completed.is_(True)
        )
    )
    completed = result.scalars().all()
    completed_count = len(completed)

    from backend.models.execution import ExecutionHistory

    result = await db.execute(
        select(ExecutionHistory).where(ExecutionHistory.user_id == user.id)
    )
    histories = result.scalars().all()
    total_submits = len(histories)

    return {
        "completed_count": completed_count,
        "total_submits": total_submits,
        "all_quest_one_shot": False,
        "best_time": None,
    }


async def get_or_create_preferences(user_id: int, db: AsyncSession) -> dict[str, str]:
    result = await db.execute(
        select(UserPreference).where(UserPreference.user_id == user_id)
    )
    prefs = result.scalars().all()
    return {p.key: p.value for p in prefs}
