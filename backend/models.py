from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    notes: Optional[str] = None
    due: Optional[datetime] = None
    deps: Optional[List[str]] = []

class Task(TaskCreate):
    id: str
    created_at: datetime
    completed: bool = False

class Plan(BaseModel):
    today: List[str] = []
    updated_at: Optional[datetime] = None
