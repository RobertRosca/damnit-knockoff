import random
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from damnit_knockoff.context_reader import RunInsert, field


class AnotherTable(RunInsert):
    @field
    def independence(self):
        return True


class SomeTable(RunInsert):
    # @field
    # def extracted_value(self):
    #     # TODO: looks like it returns the data for a run's source, but actually
    #     # saves the path within the HDF5 file, which is used later for loading
    #     return self.run["bla"]["position.value"]

    @field
    def raw(self) -> bool:
        return False

    @field
    def proc(self) -> bool:
        return False

    @field
    async def query_self_table_in_call(self) -> int:
        # This shows querying the database in a field's call method, pretty messy, can
        # be tidied up a bit but core functionality is here
        res = await SomeTable.find().sort(-SomeTable.run_no).limit(1).first_or_none()
        return res.run_no if res else 0

    @field
    async def query_other_table_in_call(self) -> bool | None:
        # Also applies to other tables:
        res = await AnotherTable.find().sort(-AnotherTable.run_no).limit(1).first_or_none()  # type: ignore
        return res.independence if res else None

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
