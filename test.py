import asyncio

from pathlib import Path

from damnit_knockoff.db import db_init
from damnit_knockoff.context_reader import MODELS


async def test():
    await db_init()

    for model in MODELS:
        latest = await model.find().sort(-model.run).limit(1).first_or_none()
        await model(
            proposal=4696,
            run=latest.run + 1 if latest else 1,
            path=Path("/gpfs/exfel/exp/HED/202321/p004696/"),
        ).insert()


if __name__ == "__main__":
    asyncio.run(test())
