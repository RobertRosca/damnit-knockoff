from starlite import Controller, Starlite, post

from damnit_knockoff.db import RunCreate, db_init
from damnit_knockoff.context_reader import MODELS


class Backend(Controller):
    path = "/trigger"

    @post()
    async def trigger(self, data: RunCreate) -> list[dict]:
        res = []
        for model in MODELS:
            instance = model(**data.dict())
            await instance.insert()  # type: ignore
            res.append(instance)
        return [r.json() for r in res]


app = Starlite(
    route_handlers=[Backend],
    on_startup=[db_init],
    debug=True,
)
