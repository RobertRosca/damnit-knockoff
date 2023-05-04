# Proof of Concept - Web Interface

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
