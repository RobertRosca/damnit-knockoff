from starlite import Starlite, get

from damnit_knockoff.db import BaseRun, db_init


@get("/")
async def index() -> list[BaseRun]:
    return await BaseRun.find_all()


app = Starlite([index])
