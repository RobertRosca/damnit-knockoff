from pathlib import Path
from typing import TYPE_CHECKING

from beanie import Document, init_beanie

if TYPE_CHECKING:
    from starlite import State


class RunBase(Document):
    """Essential information that **must** be provided to trigger a Run event."""

    proposal: int
    run: int
    path: Path


async def db_init(
    state: "State" = None,  # type: ignore
    url: str = "mongodb://localhost:27017/",
    db_name: str = "damnit",
):
    from damnit_knockoff.context_reader import MODELS
    from motor.motor_asyncio import AsyncIOMotorClient as Client

    client = Client(url)

    await init_beanie(
        database=getattr(client, db_name),
        document_models=MODELS,  # type: ignore
    )
