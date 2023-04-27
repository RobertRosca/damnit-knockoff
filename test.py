import asyncio

from damnit_knockoff.db import db_init
from damnit_knockoff.context_reader import MODELS

from icecream import ic


async def test():
    await db_init()

    for UserClass in MODELS:
        # Pretend that Kafka sent a message saying run 1 is available
        m = UserClass(proposal=1, run=1)
        # Insert the document into the database - triggering its methods
        await m.insert()

    for UserClass in MODELS:
        res = await UserClass.find_all().to_list()
        ic(UserClass.__name__)
        for entry in res:
            entry = entry.copy(exclude={"id", "revision_id"})
            ic(entry)


if __name__ == "__main__":
    asyncio.run(test())
