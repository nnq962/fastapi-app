# core/mongo.py
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from core.config import settings
from core.logging import setup_logging

# Chỉ có User Document
from modules.users.models.user import User

client: AsyncIOMotorClient | None = None

@asynccontextmanager
async def lifespan(app):
    setup_logging()
    global client
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client.get_database(settings.MONGO_DB)

    # init_beanie với User Document
    await init_beanie(database=db, document_models=[User])

    try:
        yield
    finally:
        client.close()