import asyncio

from damnit_knockoff.db import db_init
from damnit_knockoff.demo_context import SomeStuff


async def test():
    await db_init()

    stuff = SomeStuff(proposal=1, run=1, comment="hi")
    await stuff.insert()  # type: ignore

    async for thing in SomeStuff.find_all():
        print(thing)


if __name__ == "__main__":
    asyncio.run(test())
