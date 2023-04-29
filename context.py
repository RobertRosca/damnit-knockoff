import random

from damnit_knockoff.context_reader import BaseRun, field


class SomeTable(BaseRun):
    @field
    def foo(self) -> int:
        print("foo")
        return random.randint(0, 100)

    @field
    def bar(self) -> bool:
        print("bar")
        return random.randint(0, 1) == 1


class MultipleTablesWorkAccidentallyIGuess(BaseRun):
    @field
    def buzz(self) -> int:
        return 100
