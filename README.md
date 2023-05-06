# DAMNIT Knockoff

## Implementing Suggestions from Workshop

Powered by salt, I have decided to try and implement a few things that came up during the workshop to see if the ideas presented to make development easier.

Current status:

| Feature         | Status | Source       |Comments         | Commit                                   |
|-----------------|--------|--------------|-----------------|------------------------------------------|
| Multiple Tables | Yes    | Classes, ORM | Already working | 75822c2097abb828424d6e5fb7eee7c4b06187a0 |

## Summary of Ideas

### Generic

Using `dependency: Annotated[str, "var#thing"]` in DAMNIT:

- Retains both the current use of annotations with strings to define dependency on variables and type annotations.
- Can enable some additional checks on the context file editor.
- IMO pretty useful as it isn't too uncommon to get confused over if a run number/proposal number is a string `p001234` or int `1234`.
- Should just be a few small changes (if any) on the DAMNIT side.

Class structure in context file:

- Nice way to support multiple databases, if that's desired.
- Can tackle the problem of the tables being 'too crowded' by enabling separation of concerns, e.g. separate tables for different categories of variables (sample related, beam related, experimental setup related, etc...).
- Might also be a more generic step towards the requirement for a table of grouped runs and one for sample details.
- Which could be done with inheritance (this is how my demo handles it).
- Users would write `class Foo(Run)`, and the `run` object that is currently provided as the first argument to functions would be available.
- Or `class Bar(Sample)`/`class Bar(MdC)` to have sample/MyMdC info.

### ORM

Many ORMs already support event based actions:

- SQLAlchemy has a [large list](https://docs.sqlalchemy.org/en/20/orm/events.html) of event hooks.
- I would **highly recommend** at least looking through this list as a lot of it seems relevant already, not just in my fantasy theoretical future world.
  - Standard before/after insert hooks which would be useful for DAMNIT.
  - Before/after attach hooks which execute at the time of connecting to the DB, could help with parallel DB access.
  - A lot more hook types on different lifetime/object/db events.
- Beanie has way fewer hooks, but still the basic before/after ones.

ORMs features map quite well onto what Thomas showed with the DAMNIT Python API:

- Database queries done with python method calls instead of SQL, see [query docs page](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html).
  - Basic example is writing `select(User).where(User.name == "spongebob")` instead of:

    ```SQL
    SELECT user_account.id, user_account.name, user_account.fullname
    FROM user_account
    WHERE user_account.name = ?
    [...] ('spongebob',)
    ```

- Python objects are used for the queries, and also the returned values.
- The object can be modified and used to update its database entry.

ORMs (can) support `async`.

### Pydantic

> *insert generic benefits of type annotations here*

Web API integration:

- FastAPI/LiteStar/'modern' web frameworks use Pydantic to build the API schema, create endpoints, and validate returned values.
  - Validation of returned types can be very important once you have GUI elements querying the API, unexpected variable types can really fuck with JS.
- 'Modern' frameworks also heavily use classes for dependency inversion/injection throughout function calls made by an endpoint.

### Document-Oriented/Server-Based DB

- Dynamic fields.

- Direct queries to the DB remove the need to create a REST API in some cases.

## TL;DR

- Using `dependency: Annotated[str, "var#thing"]` in DAMNIT preserves current functionality and adds in the benefits of type annotation.

- [SQLAlchemy events](https://docs.sqlalchemy.org/en/20/orm/events.html) have a lot more to offer than just on insert hooks, looks like a lot of them could have applications in both the context files and the DAMNIT codebase.
- [SQLAlchemy querying](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#simple-select) looks to achieve parts of what's desired for the Python API.
- Really just skimming the [quickstart guide](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#simple-select) and seeing if anything looks useful might be a good idea.

- New-fangled Python web frameworks rely on Pydantic for a lot of their functionality, so using it would help with creating the APIs.
- Aside from defining the endpoints, Pydantic does validation which makes the web frontend design much simpler as you're sure that a query is guaranteed to return a specific type.

- Low-code frontend tools can connect directly to a database, using a server DB and connecting to it directly removes some of the need for API development.
