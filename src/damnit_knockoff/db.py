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


def get_mongo_db():
    from motor.motor_asyncio import AsyncIOMotorClient as Client

    client = Client("mongodb://localhost:27017/")

    return client.damnit


def get_beanita_db():
    from beanita import Client

    client = Client("beanita")

    return client["damnit"]


async def db_init(
    state: "State" = None,  # type: ignore
    client="beanita",
):
    from damnit_knockoff.context_reader import MODELS

    if client == "beanita":
        db = get_beanita_db()
    else:
        db = get_mongo_db()

    await init_beanie(
        database=db,
        document_models=MODELS,  # type: ignore
    )
