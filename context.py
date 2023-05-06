import random
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from xarray import DataArray, Dataset

from damnit_knockoff.context_reader import RunBase, field


class SomeTable(RunBase):
    # @field
    # def extracted_value(self):
    #     # TODO: looks like it returns the data for a run's source, but actually
    #     # saves the path within the HDF5 file, which is used later for loading
    #     return self.run["bla"]["position.value"]


    # @field
    # def random_plotly_schema(self) -> str:
    #     N = 100
    #     random_x = np.linspace(0, 1, N)
    #     random_y0 = np.random.randn(N) + 5
    #     random_y1 = np.random.randn(N)
    #     random_y2 = np.random.randn(N) - 5

    #     # Create traces
    #     fig = go.Figure()
    #     fig.add_trace(go.Scatter(x=random_x, y=random_y0, mode="lines", name="lines"))
    #     fig.add_trace(
    #         go.Scatter(
    #             x=random_x, y=random_y1, mode="lines+markers", name="lines+markers"
    #         )
    #     )
    #     fig.add_trace(
    #         go.Scatter(x=random_x, y=random_y2, mode="markers", name="markers")
    #     )
    #     return fig.to_json()  # type: ignore
