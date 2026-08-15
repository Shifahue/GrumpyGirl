from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class FocusPayload(BaseModel):
    task_id: str

@router.post("/focus/start")
async def focus_start(payload: FocusPayload):
    return {"status": "started", "task_id": payload.task_id, "started_at": datetime.utcnow().isoformat()}

@router.post("/focus/end")
async def focus_end(payload: FocusPayload):
    return {"status": "ended", "task_id": payload.task_id, "ended_at": datetime.utcnow().isoformat()}
