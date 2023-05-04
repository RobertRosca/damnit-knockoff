from pathlib import Path
from typing import TYPE_CHECKING

from beanie import Document, init_beanie
from pydantic import BaseModel

if TYPE_CHECKING:
    from starlite import State


class RunCreate(BaseModel):
    """Essential information that **must** be provided to trigger a Run event."""

    proposal: int
    run: int
    path: Path


class Run(RunCreate, Document):
    """Optional information that is commonly added."""

    comment: str | None = None


async def db_init(
    state: "State" = None,  # type: ignore
    url: str = "mongodb://localhost:27017/",
    db_name: str = "damnit",
    db_type: str = "motor",
):
    from damnit_knockoff.context_reader import MODELS

    # From messing with different client types
    match db_type:
        case "motor":
            from motor.motor_asyncio import AsyncIOMotorClient as Client
        case "mongita":
            from mongita import MongitaClientDisk as Client
        case "beanita":
            from beanita import Client
        case _:
            raise Exception()

    client = Client(url)

    await init_beanie(
        database=getattr(client, db_name),
        document_models=MODELS,  # type: ignore
    )
