import asyncio

from damnit_knockoff.db import db_init
from damnit_knockoff.context_reader import MODELS


async def test():
    await db_init()

    for model in MODELS:
        print(f"Inserting fake data into {model.__name__}")
        await model(proposal=1, run=1, comment="hi").insert()

    for model in MODELS:
        res = await model.find_all().to_list()
        print(f"Found {len(res)} entries in {model.__name__}")
        for entry in res:
            print(f"  - {entry}")


if __name__ == "__main__":
    asyncio.run(test())
