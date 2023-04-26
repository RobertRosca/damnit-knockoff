import random

from beanie import Insert, before_event

from damnit_knockoff.db import BaseRun


class SomeStuff(BaseRun):
    custom_thing: int | None = None
    potato: bool | None = None

    @before_event(Insert)
    def calculate_thing(self):
        self.custom_thing = random.randint(0, 100)

    @before_event(Insert)
    def calculate_more_things(self):
        self.potato = random.randint(0, 1) == 1
