import random

from damnit_knockoff.context_reader import BaseRun


class SomeTable(BaseRun):
    def foo(self) -> int:
        print("bonk")
        return random.randint(0, 100)

    def bar(self) -> bool:
        return random.randint(0, 1) == 1


class MultipleTablesWorkAccidentallyIGuess(BaseRun):
    def buzz(self) -> int:
        return 100
