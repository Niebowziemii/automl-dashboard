"""Prices distribution plot."""
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from plotly import graph_objs as go

if TYPE_CHECKING:
    from pandas import DataFrame
    from streamlit.delta_generator import DeltaGenerator



def plot(data: dict[str, DataFrame], module: DeltaGenerator) -> None:
    """Distribution of prices.

    Args:
        data (DataFrame): DataFrame containing price data.
        module (DeltaGenerator): Layout element for rendering.
    """
    available_states = list(data["stv"]["state_id"].unique())
    selected_states = module.multiselect(
        "Select state:",
        available_states,
        available_states,
    )

    available_stores = list(
        filter(
            lambda store: store.startswith(tuple(selected_states)),
            list(data["stv"]["store_id"].unique()),
        )
    )
    selected_stores = module.multiselect("Select store:", available_stores, available_stores)

    available_categories = list(data["stv"]["cat_id"].unique())
    selected_categories = module.multiselect(
        "Select category:",
        available_categories,
        available_categories,
    )

    filtered_sp = data["sp"][
        data["sp"]["store_id"].isin(selected_stores) &
        data["sp"]["item_id"].str.startswith(tuple(selected_categories))
        ]

    if len(filtered_sp) == 0:
        module.warning("No data available.")
        return

    maximum_value = 31

    fig = go.Figure()
    fig.update_layout(
        title_text="Distribution of sell prices",
        xaxis_title_text="Sell price",
        yaxis_title_text="Count",
        bargap=0.2,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1,  # gap between bars of the same location coordinate.
        xaxis={
            "tickmode": "array",
            "tickvals": list(range(maximum_value + 1)),
            "ticktext": [str(i) for i in range(maximum_value)] + list(">"),
        }
    )

    fig.add_trace(
        go.Histogram(
            x=[np.minimum(maximum_value, num) for num in filtered_sp["sell_price"]],
            xbins={"size": 1},
        )
    )

    module.plotly_chart(fig)
