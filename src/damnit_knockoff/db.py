from pathlib import Path
from typing import TYPE_CHECKING

from beanie import Document, init_beanie
from pydantic import BaseModel, Extra

if TYPE_CHECKING:
    from starlite import State


class RunCreate(BaseModel):
    proposal: int
    run: int
    path: Path


class Run(RunCreate, Document, extra=Extra.allow):
    comment: str | None = None


async def db_init(
    state: "State" = None,  # type: ignore
    url: str = "mongodb://localhost:27017/",
    db_name: str = "damnit",
    db_type: str = "motor",
):
    from damnit_knockoff.context_reader import MODELS

    match db_type:
        case "motor":
            from motor.motor_asyncio import AsyncIOMotorClient as Client
        case "mongita":
            from mongita import MongitaClientDisk as Client
        case "beanita":
            from beanita import Client
        case _:
            raise Exception()

    client = Client("LOCAL_DIRECTORY")

    await init_beanie(
        database=getattr(client, db_name),
        document_models=MODELS,  # type: ignore
    )
