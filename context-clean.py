import random

from damnit_knockoff.context_reader import BaseRun


def some_method() -> int:
    return random.randint(0, 100)


class SomeTable(BaseRun):
    def foo(self) -> int:
        return some_method()

    async def bar(self) -> bool:
        return random.randint(0, 1) == 1

    def oof(self) -> str | None:
        if self.bar:
            return "hello"


class MultipleTablesWorkAccidentallyIGuess(BaseRun):
    def buzz(self) -> int:
        return some_method()
