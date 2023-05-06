# DAMNIT Knockoff

This is (mostly) **not** saying I think things *should* be done differently, it's just showing a different approach with relatively new packages/design styles which might be interesting to be aware of.

Along that line, creating a demo requires picking packages and software, try to **ignore the specific choices** of software and just think about the generic points of:

- **Document-oriented databases** - this uses Mongo, there are many others, including file-based ones ;P
- **ORM/ODM** - this uses Beanie, there are many others.
- **Design choices** - lots of options which change based on the DB/OD(R)M.

## Questions and Comments

Please try to keep questions during this demo limited to ones which can be answered quickly, like a clarification, and avoid questions that can lead to longer discussions - we can have those at the end.

## Intro

After looking through the DAMNIT code the first time I had a few thoughts:

1. `Annotated` type might help clear things up a bit in the arguments, e.g. `run_no: Annotated[int, "meta#run_number"]` would have the required string annotation but still retain the real type annotation.
2. An SQL database is not the best for this since they're designed to work with stable schemas known ahead of time, not with dynamic ones. NoSQL would be better, something **like** MongoDB?
3. ORM/ODM library might help simplify the backend code, since I have experience with it I decided to use Beanie but there are a lot of other options.
4. Using ORM/ODM would help when(/if) setting up an API.
5. Async support would be very nice for some tasks.

With some of those ideas in mind I made a proof of concept that uses Beanie and MongoDB.

<!-- ## Pre-emptive Points

There are decent file-based backends for Mongo/other document-based DBs:

- <https://github.com/roman-right/beanita>
- <https://github.com/scottrogowski/mongita>
- <https://github.com/google/leveldb>

**But** there are good reasons to use a server as well, which I'll show at the end. -->
