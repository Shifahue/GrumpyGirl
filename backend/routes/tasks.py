from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

from db import db
from ai_stub import decompose_goal

router = APIRouter()

class UserCreate(BaseModel):
    device_id: Optional[str]

@router.post("/user")
async def create_user(payload: UserCreate):
    # Minimal: return a device id
    return {"user_id": payload.device_id or str(uuid.uuid4())}

class DecomposeRequest(BaseModel):
    goal: str

@router.post("/decompose")
async def decompose(req: DecomposeRequest):
    return decompose_goal(req.goal)

@router.get("/today")
async def get_today():
    # Return empty list or simple query
    docs = []
    cursor = db.tasks.find({}).sort("created_at", 1).limit(50)
    async for d in cursor:
        d["id"] = str(d.pop("_id"))
        docs.append(d)
    return docs

@router.get("/tasks")
async def list_tasks():
    docs = []
    cursor = db.tasks.find({}).sort("created_at", -1).limit(100)
    async for d in cursor:
        d["id"] = str(d.pop("_id"))
        docs.append(d)
    return docs

@router.post("/tasks")
async def create_task(payload: dict):
    t = {
        "title": payload.get("title"),
        "notes": payload.get("notes"),
        "deps": payload.get("deps", []),
        "created_at": datetime.utcnow(),
        "completed": False,
    }
    res = await db.tasks.insert_one(t)
    t["id"] = str(res.inserted_id)
    return t

@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    from bson import ObjectId
    try:
        o = ObjectId(task_id)
    except Exception:
        raise HTTPException(404, "not found")
    doc = await db.tasks.find_one({"_id": o})
    if not doc:
        raise HTTPException(404, "not found")
    doc["id"] = str(doc.pop("_id"))
    return doc

@router.patch("/tasks/{task_id}")
async def patch_task(task_id: str, payload: dict):
    from bson import ObjectId
    try:
        o = ObjectId(task_id)
    except Exception:
        raise HTTPException(404, "not found")
    await db.tasks.update_one({"_id": o}, {"$set": payload})
    doc = await db.tasks.find_one({"_id": o})
    if not doc:
        raise HTTPException(404, "not found")
    doc["id"] = str(doc.pop("_id"))
    return doc

@router.post("/tasks/{task_id}/complete")
async def complete_task(task_id: str):
    from bson import ObjectId
    try:
        o = ObjectId(task_id)
    except Exception:
        raise HTTPException(404, "not found")
    await db.tasks.update_one({"_id": o}, {"$set": {"completed": True}})
    return {"status": "ok"}

@router.post("/tasks/{task_id}/breakdown")
async def breakdown_task(task_id: str):
    # Return placeholder breakdown
    return {"suggestions": ["Break into smaller steps", "Estimate time"]}

@router.post("/tasks/{task_id}/stuck")
async def stuck_task(task_id: str):
    return {"advice": "Try the 2-minute rule: do a tiny step now."}

@router.post("/tasks/{task_id}/postpone")
async def postpone_task(task_id: str):
    return {"status": "postponed"}
