from fastapi import APIRouter
from db import db
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class PlanUpdate(BaseModel):
    today: list

@router.get("/plan")
async def get_plan():
    doc = await db.plan.find_one({}, sort=[("_id", -1)])
    if not doc:
        return {"today": []}
    doc.pop("_id", None)
    return doc

@router.put("/plan")
async def put_plan(payload: PlanUpdate):
    data = payload.dict()
    data["updated_at"] = datetime.utcnow()
    await db.plan.insert_one(data)
    return data

@router.post("/fix-my-day")
async def fix_my_day():
    # dumb implementation
    return {"plan": "Here is a suggested today list (stub)."}
