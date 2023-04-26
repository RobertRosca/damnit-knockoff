from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from damnit_knockoff.context_reader import get_models


class BaseRun(Document):
    proposal: int
    run: int
    comment: str


async def db_init(models):
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    # models = get_models()
    await init_beanie(
        database=client.db_name,
        document_models=models,  # type: ignore
    )
