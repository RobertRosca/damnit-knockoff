# DAMNIT Knockoff

After looking through the DAMNIT code the first time I had a few thoughts:

1. `Annotated` type might help clear things up a bit in the arguments, e.g. `run_no: Annotated[int, "meta#run_number"]` would have the required string annotation but still retain the real type annotation.
2. An SQL database is not the best for this since they're designed to work with stable schemas known ahead of time, not with dynamic ones. NoSQL would be better, something **like** MongoDB?
3. ORM/ODM library might help simplify the backend code, since I have experience with it I decided to use Beanie but there are a lot of other options.
4. Using ORM/ODM would help when(/if) setting up an API.
5. Async support would be very nice for some tasks.

With some of those ideas in mind I made a proof of concept that uses Beanie and MongoDB.

## Pre-emptive Points

There are decent file-based backends for Mongo/other document-based DBs:

- <https://github.com/roman-right/beanita>
- <https://github.com/scottrogowski/mongita>
- <https://github.com/google/leveldb>

**But** there are good reasons to use a server as well, which I'll show at the end.

## PoC v1

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
    """Base class with default fields - what is provided by Kafka"""
    proposal: int
    run: int
    comment: str = ""


class UserClass(BaseRun):
    """User class defined in context file"""
    foo: int | None = None  # Define fields first
    bar: list | None = None
    baz: dict[str, int] | None = None
    bop: str

    @before_event(Insert)  # Beanie has before/after event decorators
    async def _bop(self):  # User defined method
        asyncio.sleep(1)  # Async
        self.bop = "Ooo async"  # Setting a field

    @before_event(Insert)
    def _foo(self):
        self.foo = 10

    @before_event(Insert)
    def _bar(self):
        self.bar = [10, 2, 3]  # List support

    @before_event(Insert)
    def _baz(self):
        self.baz = {"hi": 2}  # Dict support


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

    # Triggers the methods decorated with `@before_event(Insert)`
    await uc.insert()
    print(f"{uc}")

    res = await UserClass.find_all().to_list()
    pprint(res)


if __name__ == "__main__":
    asyncio.run(test())
```

Benefits of this approach are kind of spread across different sources:

### Benefit from the implementation

- Class structure is more flexible, supports multiple collections (tables) out of the box - allows for separation of user data.

### Benefit from Document-Oriented DB

- Collections (tables) do not have a schema, documents in a collection can have different fields, adding/removing fields is is simple.
- More field types supported than sqlite: list, bytes, tuple, dict, set, enum, datetime, namedtuple, path, uuid, probably more.
- Nested documents are also possible.
- Very nice time-series data support.

- Lazy parsing/loading of documents.
- Fancy indexing, e.g. multi-field indexes.
- Revision support and state management, helps avoid data loss/overwriting during concurrent operations.

### Benefit from Beanie

- Inheritance (of the classes), more complex collections can be set up which inherit shared attributes from parent classes.
- No need for additional code to handle dynamically adding in columns based on the user provided context file.
- Handles the event-based method calls: `Insert`, `Replace`, `Update`, `SaveChanges`, `Delete`, `ValidateOnSave`.
- Multiple directions supported: `before` and `after`.
- `async` support.

And from Pydantic (which Beanie heavily uses):

- By validating the types you can write frontend/GUI features more easily since you know what data you'll get from the DB.
- (list of all normal benefits of type aliases here)...
- Nice IDE integration I guess - enhances the warnings showed by the context file editor.
- BUT this can probably be achieved with `Annotated[type, "damnit#string"]`.

## PoC v2

Builds on top of the initial one:

- Loads user code from separate context file via `importlib`
- Attempts to simplify the style of the context files by:
  1. Extracting relevant classes and methods.
  2. Automatically applying decorators:
    1. One is the `pseudo_property_decorator`, which is similar to `@property` in that it runs a method one time and then sets that method equal to its return value.
    2. The next decorator is `before_event(Insert)`, which is what was previously applied manually.

Benefits:

- Demonstrates that it is still possible to make the context files look fairly simple and independent of the backend/db with not too much effort/complex code.
- (debatably a benefit) removes the need for the `@Variable` decorator.

## PoC v2.5

The automatic application of these decorators is kind of weird, I did it to see how it would work since the concept seemed interesting. This version is basically the same as the previous version, but without the automatic decorators.

Benefits:

- Decorators can have arguments, e.g. `direction` to set if the method gets called before or after events.
- Class methods without decorator are not treated as fields automatically, which is a bit more reasonable.

**Note** - I stuck to using class definitions in the context file since that gives an easy way to define **multiple collections**, but it is of course possible to remove that feature and have a single collection for the context file as is currently done.

## PoC v3

- Add crappy REST API to make triggering easier.
- Make the context file more complex.
- Add a terrible web frontend demo.

Benefits:

- More benefits of Document-oriented DBs really come out now:
  - Frontend can dynamically add fields without needing to do anything with the context file
  - Ability to add fields within a method call can be useful

- Frontends can have (broadly) three ways to interact with a DB, all of which benefit from parts of this approach:
  1. Direct connection to a DB server - Mongo server is available - of course some SQL server provides the same benefit.
  2. Call to an API - arguably easier to set up APIs with Pydantic-based ORM/ODMs.
  3. Server side rendering of page - ORM/ODMs make interacting with DB objects simpler.
