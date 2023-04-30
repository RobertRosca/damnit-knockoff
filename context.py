import random

from beanie import after_event

from damnit_knockoff.context_reader import BaseRun, field


class SomeTable(BaseRun):
    def method(self):
        print("bonk")

    @field
    def foo(self) -> int:
        print("foo")
        return random.randint(0, 100)

    @field(direction=after_event)
    def bar(self) -> bool:
        print("bar")
        return random.randint(0, 1) == 1


class MultipleTablesWorkAccidentallyIGuess(BaseRun):
    @field
    def buzz(self) -> int:
        return 100
