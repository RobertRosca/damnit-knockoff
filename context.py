import random

from damnit_knockoff.context_reader import BaseRun

# Users can define methods, which are not called but can be used in the classes
def some_method() -> int:
    return random.randint(0, 100)

# Users can define classes, which are used to create documents (tables) in mongo
class SomeTable(BaseRun):
    # Class methods are parsed and used to create fields in the document, e.g
    # def foo(self) -> int will create a field called foo with type int
    # Methods are called before the document is inserted into the database
    def foo(self) -> int:
        return some_method()

    # Async methods are also supported
    async def bar(self) -> bool:
        return random.randint(0, 1) == 1

    def oof(self) -> str | None:
        if self.bar:
            return "hello"

# Users can define multiple classes in the same file, and they will all be used
# to create multiple tables in the database
class MultipleTablesWorkAccidentallyIGuess(BaseRun):
    def buzz(self) -> int:
        return some_method()
