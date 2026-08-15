import os
from motor.motor_asyncio import AsyncIOMotorClient

client: AsyncIOMotorClient | None = None
db = None

async def connect_db():
    global client, db
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(mongo_url)
    db_name = os.environ.get("DB_NAME", "grumpygirl")
    db = client[db_name]

async def close_db():
    global client
    if client:
        client.close()
