"""Sales distribution plot."""
from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.express as px
from pandas import DataFrame

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator

from src.plots.helper import helper_func


def plot(data: dict[str, DataFrame], module: DeltaGenerator, key_s: str) -> None:
    """Distribution of sales.

    Args:
        data (dict[str, DataFrame]): M5 forecasting accuracy dict formatted as in load.py.
        module (DeltaGenerator): Layout element for rendering.
        key_s (str): Key for streamlit components.
    """
    n = 1000

    available_states = list(data["stv"]["state_id"].unique())
    selected_states = module.multiselect("Select state:", available_states, available_states, key=key_s + "0")

    available_stores = list(
        filter(
            lambda store: store.startswith(tuple(selected_states)),
            list(data["stv"]["store_id"].unique()),
        )
    )
    selected_stores = module.multiselect("Select store:", available_stores, available_stores, key=key_s + "1")

    available_categories = list(data["stv"]["cat_id"].unique())
    selected_categories = module.multiselect("Select category:", available_categories, available_categories, key=key_s + "2")

    filtered_stv = data["stv"].query(f"state_id in {selected_states} & store_id in {selected_stores} & cat_id in {selected_categories}")

    if len(filtered_stv) == 0:
        module.warning("No data available.")
        return

    sample_stv = filtered_stv if len(filtered_stv) < n else filtered_stv.sample(n=n, random_state=42)

    merged = helper_func(sample_stv).merge(data["calendar"], how="left", left_on="dates", right_on="d")

    merged_ = DataFrame(merged.groupby("date")["sales"].sum()).reset_index()

    fig = px.line(
        merged_,
        x="date",
        y="sales",
        title=f"Sales over time of random {n} products",
        labels={"date": "Date", "sales": "Sales"},
        render_mode="webg1",
    )

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector={
            "buttons": [
                {"count": 1, "label": "1m", "step": "month", "stepmode": "backward"},
                {"count": 3, "label": "3m", "step": "month", "stepmode": "backward"},
                {"count": 6, "label": "6m", "step": "month", "stepmode": "backward"},
                {"count": 1, "label": "1y", "step": "year", "stepmode": "backward"},
                {"step": "all"},
            ]
        },
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeselector_font_color="white",
        xaxis_rangeselector_activecolor="red",
        xaxis_rangeselector_bgcolor="black",
    )

    module.plotly_chart(fig)
