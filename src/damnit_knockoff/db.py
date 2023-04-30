from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from damnit_knockoff.context_reader import MODELS


async def db_init():
    client = AsyncIOMotorClient("mongodb://localhost:27017/")
    await init_beanie(
        database=client.damnit,
        document_models=MODELS,  # type: ignore
    )
