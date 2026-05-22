from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from backend.database import Base


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quest_id = Column(String(20), nullable=False)
    completed = Column(Boolean, default=False)
    completed_tasks = Column(String(500), default="")
    completed_at = Column(DateTime(timezone=True), nullable=True)

    @property
    def completed_task_list(self) -> list[str]:
        return self.completed_tasks.split(",") if self.completed_tasks else []

    def add_completed_task(self, task_id: str) -> None:
        tasks = set(self.completed_task_list)
        tasks.add(task_id)
        self.completed_tasks = ",".join(sorted(tasks))
