from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str


class UserResponse(BaseModel):
    id: int
    username: str
    xp: int
    level: int
    coins: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
