import datetime
from pathlib import Path

from damnit_knockoff.context_reader import BaseRun, field
import plotly.express as px


import random


class SomeTable(BaseRun):
    @field
    def created_at(self) -> datetime.datetime:
        return datetime.datetime.now()

    @field
    def files_in_raw(self) -> int:
        return len(list((self.path / "raw" / f"r{self.run:04d}").glob("*")))

    @field
    def raw_run_dir(self) -> Path:
        return self.path / "raw" / f"r{self.run:04d}"

    @field
    def random_list(self) -> list | None:
        return [{"x": str(x), "y": random.random() * x} for x in range(1, 100)]

    @field
    def html_plot(self) -> str | None:
        fig = px.scatter(x=range(100), y=[random.random() * x for x in range(100)])
        return fig.to_html(include_plotlyjs="cdn")
