import asyncio
import datetime
import random

from beanie import Insert, after_event, before_event

from damnit_knockoff.db import BaseRun, db_init


class SomeStuff(BaseRun):
    custom_thing: int | None = None
    potato: bool | None = None
    foo: str | None = None

    @before_event(Insert)
    async def calculate_thing(self):
        self.custom_thing = random.randint(0, 100)

    @before_event(Insert)
    async def calculate_more_things(self):
        self.potato = random.randint(0, 1) == 1

    @after_event(Insert)
    async def calculate_slow_things(self):
        self.foo = datetime.datetime.utcnow().isoformat()
        await asyncio.sleep(2)
        await self.replace()


async def test():
    await db_init([SomeStuff])

    stuff1 = SomeStuff(proposal=1, run=1, comment="hi")
    stuff2 = SomeStuff(proposal=1, run=2, comment="hi")

    await asyncio.gather(stuff1.insert(), stuff2.insert())

    async for stuff in SomeStuff.find_all():
        print(stuff)


if __name__ == "__main__":
    asyncio.run(test())
