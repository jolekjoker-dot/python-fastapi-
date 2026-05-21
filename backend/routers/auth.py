from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from backend.database import get_db
from backend.models.user import User
from backend.schemas.user import TokenResponse, UserCreate, UserResponse
from backend.services.auth_service import create_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == data.username))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(username=data.username)
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        user.last_login = func.now()
        await db.commit()
        await db.refresh(user)

    token = create_token(user.id)
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
