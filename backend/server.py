from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from routes import tasks, plan, focus
from db import connect_db, close_db

app = FastAPI(title="grumpygirl API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await connect_db()

@app.on_event("shutdown")
async def on_shutdown():
    await close_db()

app.include_router(tasks.router, prefix="/api")
app.include_router(plan.router, prefix="/api")
app.include_router(focus.router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok"}
