import random
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from damnit_knockoff.context_reader import RunBase, field


class SomeTable(RunBase):
    @field
    def thing(self) -> str:
        return "hi"

    @field
    def raw_run_dir(self) -> Path:
        return self.path / "raw" / f"r{self.run:04d}"

    @field
    def size(self) -> float:
        return random.random() * 1000

    @field
    def random_list(self) -> list:
        return [random.random() for x in range(8)]

    @field
    def random_dict(self) -> dict:
        return {"hello": "world", "random": random.random()}

    @field
    def random_plotly_schema(self) -> str:
        N = 100
        random_x = np.linspace(0, 1, N)
        random_y0 = np.random.randn(N) + 5
        random_y1 = np.random.randn(N)
        random_y2 = np.random.randn(N) - 5

        # Create traces
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=random_x, y=random_y0, mode="lines", name="lines"))
        fig.add_trace(
            go.Scatter(
                x=random_x, y=random_y1, mode="lines+markers", name="lines+markers"
            )
        )
        fig.add_trace(
            go.Scatter(x=random_x, y=random_y2, mode="markers", name="markers")
        )
        return fig.to_json()  # type: ignore
