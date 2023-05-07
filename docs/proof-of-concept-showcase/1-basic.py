import asyncio
from pprint import pprint

from beanie import Document, Insert, before_event, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Extra


class BaseRun(Document):
    proposal: int
    run: int
    comment: str = ""


class UserClass(BaseRun, extra=Extra.allow):
    foo: int | None = None
    bar: list | None = None
    baz: dict[str, int] | None = None
    bop: str | None = None
    n: set = {1, 2}

    @before_event(Insert)
    def _foo(self):
        print("Foo set")
        self.foo = 10

    @before_event(Insert)
    def _bar(self):
        print("Bar set")
        self.bar = [10, 2, 3]

    @before_event(Insert)
    def _baz(self):
        print("Baz set")
        self.baz = {"hi": 2}

    @before_event(Insert)
    async def _bop(self):
        print("Bop sleep")
        await asyncio.sleep(1)
        self.bop = "Ooo async"
        print("Bop done")

    @before_event(Insert)
    async def _bop2(self):
        print("Bop2 sleep")
        await asyncio.sleep(1)
        self.bop = "Spooky"
        print("Bop2 done")


async def db_init():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(
        database=client.db_name,
        document_models=[UserClass],  # type: ignore
    )


async def test():
    await db_init()

    # Pretend Kafka notification comes in with this information:
    uc = UserClass(proposal=1, run=1)  # type: ignore
    print(f"{uc=}")

    await uc.insert()  # type: ignore
    print(f"{uc}")

    res = await UserClass.find_all().to_list()  # type: ignore
    pprint(res)


if __name__ == "__main__":
    asyncio.run(test())
