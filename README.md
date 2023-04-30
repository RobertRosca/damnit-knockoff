# DAMNIT Knockoff

After looking through the DAMNIT code the first time I had a few thoughts:

1. `Annotated` type might help clear things up a bit in the arguments, e.g. `run_no: Annotated[int, "meta#run_number"]` would have the required string annotation but still retain the real type annotation.
2. An SQL database is not the best for this since they're designed to work with stable schemas known ahead of time, not with dynamic ones. NoSQL would be better, something like MongoDB?
3. ORM/ODM library might help simplify the backend code, since I have experience with it I decided to use Beanie but there are a lot of other options.
4. Using ORM/ODM would help when(/if) setting up an API.
5. Async support would be very nice for some tasks

With some of those ideas in mind I made a proof of concept that uses Beanie and MongoDB.

## First Super Basic PoC

For this to be vaguely coherent, I'll go through a few different stages during the design and build up the complexity gradually instead of showing the final version from the start.

The super-duper basic proof of concept for this is very simple but:

1. Shows the basic concepts of user-defined collections (equivalent to a table).
2. Where the fields (variables) can be set by functions/methods.
3. And these functions run when a new document (a record, basic 'unit of data' in mongo, like a row) is being inserted to the DB.

```python
import asyncio
from beanie import Document, Insert, before_event, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from pprint import pprint


class BaseRun(Document):
    proposal: int
    run: int
    comment: str = ""


class UserClass(BaseRun):
    foo: int | None = None
    bar: list | None = None
    baz: dict[str, int] | None = None
    bop: str

    @before_event(Insert)
    async def _bop(self):
        asyncio.sleep(1)
        self.bop = "Ooo async"

    @before_event(Insert)
    def _foo(self):
        self.foo = 10

    @before_event(Insert)
    def _bar(self):
        self.bar = [10, 2, 3]

    @before_event(Insert)
    def _baz(self):
        self.baz = {"hi": 2}



async def db_init():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(
        database=client.db_name,
        document_models=[UserClass],  # type: ignore
    )


async def test():
    await db_init()

    # Pretend Kafka notification comes in with this information:
    uc = UserClass(proposal=1, run=1)
    print(f"{uc=}")

    await uc.insert()
    print(f"{uc}")

    res = await UserClass.find_all().to_list()
    pprint(res)


if __name__ == "__main__":
    asyncio.run(test())
```

Benefits of this approach:

1. Type validation via Pydantic.
2. Beanie does 99% of the work for us.
3. Class structure is more flexible, supports multiple collections (tables) out of the box.
4. Multiple events supported: `Insert`, `Replace`, `Update`, `SaveChanges`, `Delete`, `ValidateOnSave`.
5. Multiple directions supported: `before` and `after`.
6. `async` support.
7. And a lot of nice features from using Mongo/Beanie, actually useful:
    1. Collections (tables) do not have a schema, documents in a collection can have different fields, adding/removing fields is is simple.
    2. More field types supported than sqlite: list, bytes, tuple, dict, set, enum, datetime, namedtuple, path, uuid, probably more.
    3. Inheritance, more complex collections can be set up which inherit shared attributes from parent classes.
    4. Nested documents are also possible.
    5. Very nice time-series data support.
8. Potentially useful:
    1. Lazy parsing/loading of documents.
    2. Fancy indexing, e.g. multi-field indexes.
    3. Revision support and state management, helps avoid data loss/overwriting during concurrent operations.

## Second PoC

Builds on top of the initial one:

1. Loads user code from separate context file via `importlib`
2. Attempts to 'simplify' the style of the context files by:
    1. Extracting relevant classes and methods.
    2. Automatically applying decorators
        1. One is the `pseudo_property_decorator`, which is similar to `@property` in that it runs a method one time and then sets that method equal to its return value.
        2. The next decorator is `before_event(Insert)`, which is what was previously applied manually.

Benefits:

1. Demonstrates that it is still possible to make the context files look fairly simple and independent of the backend/db with not too much effort/complex code.
2. (debatably a benefit) Removes the need for the `@Variable` decorator.

## Second (and a half) PoC

The automatic application of these decorators is kind of weird, I did it to see how it would work since the concept seemed interesting. This version is basically the same as the previous version, but without the automatic decorators.

Benefits:

1. Decorators can have arguments, e.g. `direction` to set if the method gets called before or after events.
2. Class methods without decorator are not treated as fields automatically, which is a bit more reasonable.

**Note** - I stuck to using class definitions in the context file since that gives an easy way to define multiple collections, but it is of course possible to remove that feature and have a single collection for the context file as is currently done.

## SQS Call 08:36

- SQS doing scans with multi scan tool in Karabo
- Scanning position of linear delay stage
- When some seemingly random positions get scanned the delay stage does not move
- This only ever happens for one step, the next step works correctly after
- Checked that the delay stage is not physically blocked - when clicking the button to move it does move correctly
- They suspect that the scanning tool has some error
- Its history says that the step occurred but it does not actually move anything
- It is moving SQS_ILH_LAS/MDL/DELAY_AX_800

- Asked if they can continue scanning while we investigate
- Said that yeah it's fine

- Previously happened around 06:09

## SQS Call 11:02

SA3_XTD10_PES/ADC/1

Related to https://redmine.xfel.eu//issues/117846

- Problem with digitiser collecting PES from SASE3
- Digitiser crashing every few minutes
- When/if it crashes during data acquisition it would be an issue

- Started w/ long trace for all boards which were interleaved
- 2.4 million points per trace, 8 traces
- Cut down to 2 million
- Removed interleaved for 3/4 boards, only 1 interleaved
- Disabled all channels that are not required
- Collecting minimum possible amount of data
- Still crashing

- Device not currently being used, can start/stop/restart as required

## HED 11:52

- DAMNIT crashed
- 4696, 375 was good but 376 was
- It has now started working!
