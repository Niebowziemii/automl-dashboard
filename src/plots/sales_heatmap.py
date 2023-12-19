"""Sales heatmap plot."""
from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.express as px

if TYPE_CHECKING:
    from pandas import DataFrame
    from streamlit.delta_generator import DeltaGenerator


def plot(data: dict[str, DataFrame], module: DeltaGenerator, key_s: str) -> None:  # noqa: ARG001
    """Sales heatmap of smaples over time.

    Args:
        data (dict[str, DataFrame]): M5 forecasting accuracy dict formatted as in load.py.
        module (DeltaGenerator): Layout element for rendering.
        key_s (str): Key for streamlit components.
    """
    n = 100
    d = 300
    stv_ = data["stv"].sample(n=n, random_state=42)
    stv_random = stv_.drop(["id", "dept_id", "cat_id", "store_id", "state_id"], axis=1)
    stv_random = stv_random.groupby("item_id").sum()
    stv_random = stv_random.iloc[:, 1 : d + 1]
    fig = px.imshow(
        stv_random,
        color_continuous_scale=px.colors.sequential.Turbo,
        title=f"Sales Heatmap of random {n} Samples over {d} days",
        labels={"x": "Days", "y": "Products", "color": "Sales"},
    )
    fig.update_yaxes(showticklabels=False)
    module.plotly_chart(fig)
