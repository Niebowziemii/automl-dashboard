"""Sales distribution plot."""
from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.express as px
from pandas import DataFrame

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator

from src.plots.helper import helper_func


def plot(data: dict[str, DataFrame], module: DeltaGenerator) -> None:
    """Distribution of sales.

    Args:
        data (dict[str, DataFrame]): M5 forecasting accuracy dict formatted as in load.py.
        module (DeltaGenerator): Layout element for rendering.
    """
    n = 100
    stv_ = data["stv"].sample(n=n, random_state=42)

    stv_random = helper_func(stv_)

    merged = stv_random.merge(data["calendar"], how="left", left_on="dates", right_on="d")

    merged_ = DataFrame(merged.groupby("date")["sales"].sum()).reset_index()

    fig = px.line(merged_, x="date", y="sales", title=f"Sales Distribution of random {n} Samples", color_discrete_map={"color": "red"})
    module.plotly_chart(fig)
