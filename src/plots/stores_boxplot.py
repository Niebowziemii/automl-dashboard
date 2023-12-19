"""Stores boxplot."""
from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.express as px

if TYPE_CHECKING:
    from pandas import DataFrame
    from streamlit.delta_generator import DeltaGenerator


def plot(data: dict[str, DataFrame], module: DeltaGenerator, key_s: str) -> None:  # noqa: ARG001
    """Sales per store per category of random n Samples.

    Args:
        data (dict[str, DataFrame]): M5 forecasting accuracy dict formatted as in load.py.
        module (DeltaGenerator): Layout element for rendering.
        key_s (str): Key for streamlit components.
    """
    n = 100
    stv_ = data["stv"].sample(n=n, random_state=42)
    stv_random = stv_.drop(["id", "item_id", "dept_id", "state_id"], axis=1)
    stv_random = stv_random.melt(id_vars=["store_id", "cat_id"], var_name="date", value_name="sales")
    stv_random = stv_random.groupby(["store_id", "cat_id", "date"]).sum().reset_index()
    fig = px.box(
        stv_random, x="store_id", y="sales", color="cat_id", title=f"Sales per store per category of random {n} Samples", labels={"x": "Store", "y": "Sales in different days"}
    )
    module.plotly_chart(fig)
