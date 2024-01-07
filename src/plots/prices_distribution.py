"""Prices distribution plot."""
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import numpy as np
from plotly import graph_objs as go

if TYPE_CHECKING:
    from pandas import DataFrame
    from streamlit.delta_generator import DeltaGenerator


def plot(data: dict[str, DataFrame], module: DeltaGenerator, key_s: str) -> None:
    """Distribution of prices.

    Args:
        data (DataFrame): DataFrame containing price data.
        module (DeltaGenerator): Layout element for rendering.
        key_s (str): Key for streamlit components.
    """
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

    available_subcategories = list(
        filter(
            lambda subcategory: subcategory.startswith(tuple(selected_categories)),
            list(data["stv"]["dept_id"].unique()),
        )
    )
    selected_subcategories = module.multiselect("Select subcategory:", available_subcategories, available_subcategories, key=key_s + "3")

    min_date = data["calendar"][data["calendar"]["wm_yr_wk"] == data["sp"]["wm_yr_wk"].min()]["date"].to_numpy()[0]
    max_date = data["calendar"][data["calendar"]["wm_yr_wk"] == data["sp"]["wm_yr_wk"].max()]["date"].to_numpy()[-1]
    min_date = datetime.datetime.strptime(min_date, "%Y-%m-%d").astimezone()
    max_date = datetime.datetime.strptime(max_date, "%Y-%m-%d").astimezone()

    start_date = module.date_input("Start date", min_value=min_date, max_value=max_date, value=min_date, format="YYYY-MM-DD", key=key_s + "5")
    end_date = module.date_input("End date", min_value=min_date, max_value=max_date, value=max_date, format="YYYY-MM-DD", key=key_s + "6")

    # chack type of start_date and end_date:
    if type(start_date) == datetime.date and type(end_date) == datetime.date:
        start_date = data["calendar"][data["calendar"]["date"] == start_date.strftime("%Y-%m-%d")]["wm_yr_wk"].to_numpy()[0]
        end_date = data["calendar"][data["calendar"]["date"] == end_date.strftime("%Y-%m-%d")]["wm_yr_wk"].to_numpy()[-1]
    else:
        start_date, end_date = None, None

    filtered_sp = data["sp"][
        (data["sp"]["wm_yr_wk"] >= start_date)
        & (data["sp"]["wm_yr_wk"] <= end_date)
        & data["sp"]["store_id"].isin(selected_stores)
        & data["sp"]["item_id"].str.startswith(tuple(selected_subcategories))
    ]

    if len(filtered_sp) == 0:
        module.warning("No data available.")
        return

    # Choose aggregation type
    aggregation_type = module.radio("Choose Aggregation Type", ["Min", "Max", "Average"], key=key_s + "4")

    if aggregation_type == "Min":
        filtered_sp = filtered_sp.groupby("item_id")["sell_price"].min().reset_index()
    elif aggregation_type == "Max":
        filtered_sp = filtered_sp.groupby("item_id")["sell_price"].max().reset_index()
    elif aggregation_type == "Average":
        filtered_sp = filtered_sp.groupby("item_id")["sell_price"].mean().reset_index()

    maximum_value = 31

    fig = go.Figure()
    fig.update_layout(
        title_text="Distribution of sell prices",
        xaxis_title_text="Sell price (in Dollars)",
        yaxis_title_text="Count",
        bargap=0.2,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1,  # gap between bars of the same location coordinate.
        xaxis={
            "tickmode": "array",
            "tickvals": list(range(maximum_value + 1)),
            "ticktext": [str(i) for i in range(maximum_value)] + list(">"),
        },
    )

    fig.add_trace(
        go.Histogram(
            x=[np.minimum(maximum_value, num) for num in filtered_sp["sell_price"]],
            xbins={"size": 1},
        )
    )

    module.plotly_chart(fig)
