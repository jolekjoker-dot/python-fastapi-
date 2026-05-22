from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from backend.database import Base


class ExecutionHistory(Base):
    __tablename__ = "execution_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quest_id = Column(String(20), nullable=False)
    task_id = Column(String(20), nullable=False)
    code = Column(Text, default="")
    stdout = Column(Text, default="")
    stderr = Column(Text, default="")
    passed = Column(Boolean, default=False)
    execution_time = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CodeDraft(Base):
    __tablename__ = "code_drafts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quest_id = Column(String(20), nullable=False)
    task_id = Column(String(20), nullable=False)
    code = Column(Text, default="")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key = Column(String(50), nullable=False)
    value = Column(String(200), default="")
