from typing import Union, cast
from starlite import Controller, Starlite, post, get

from damnit_knockoff.db import RunBase, RunBase, db_init
from damnit_knockoff.context_reader import MODELS


class Health(Controller):
    """Check health."""

    path = "/health"

    @get()
    async def get(self) -> bool:
        return True


class Backend(Controller):
    path = "/trigger"

    @post()
    async def trigger(self, data: RunBase) -> dict[str, Union[*MODELS]]:
        res = []
        for model in MODELS:
            model = cast(RunBase, model)
            instance = model(**data.dict())
            await instance.insert()  # type: ignore
            res.append(instance)
        return [r.json() for r in res]


app = Starlite(
    route_handlers=[Health, Backend],
    # on_startup=[db_init],
    debug=True,
)
