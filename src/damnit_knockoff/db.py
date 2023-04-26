import sys
from beanie import Document, UnionDoc, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import inspect


class BaseRun(Document):
    proposal: int
    run: int
    comment: str


def get_models():
    from . import demo_context

    classes = inspect.getmembers(sys.modules[demo_context.__name__], inspect.isclass)
    return [c[1] for c in classes if issubclass(c[1], (Document, UnionDoc))]


async def db_init():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(
        database=client.db_name,
        document_models=get_models(),  # type: ignore
    )
