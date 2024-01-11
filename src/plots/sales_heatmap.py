"""Sales heatmap plot."""
from __future__ import annotations
import datetime

from typing import TYPE_CHECKING

import plotly.express as px

if TYPE_CHECKING:
    from pandas import DataFrame
    from streamlit.delta_generator import DeltaGenerator


def plot(
    data: dict[str, DataFrame], module: DeltaGenerator, key_s: str
) -> None:  # noqa: ARG001
    """Sales heatmap of smaples over time.

    Args:
        data (dict[str, DataFrame]): M5 forecasting accuracy dict formatted as in load.py.
        module (DeltaGenerator): Layout element for rendering.
        key_s (str): Key for streamlit components.
    """
    n = 100

    left_column, rigth_column = module.columns(2)

    available_states = list(data["stv"]["state_id"].unique())
    selected_states = left_column.multiselect(
        "Select state:", available_states, available_states, key=key_s + "0"
    )

    available_stores = list(
        filter(
            lambda store: store.startswith(tuple(selected_states)),
            list(data["stv"]["store_id"].unique()),
        )
    )
    selected_stores = rigth_column.multiselect(
        "Select store:", available_stores, available_stores, key=key_s + "1"
    )

    available_categories = list(data["stv"]["cat_id"].unique())
    selected_categories = left_column.multiselect(
        "Select category:", available_categories, available_categories, key=key_s + "2"
    )

    available_subcategories = list(
        filter(
            lambda subcategory: subcategory.startswith(tuple(selected_categories)),
            list(data["stv"]["dept_id"].unique()),
        )
    )
    selected_subcategories = rigth_column.multiselect(
        "Select subcategory:",
        available_subcategories,
        available_subcategories,
        key=key_s + "3",
    )

    filtered_stv = data["stv"].query(
        f"state_id in {selected_states} & store_id in {selected_stores} & cat_id in {selected_categories} & dept_id in {selected_subcategories}"
    )

    total_available_days = len(data["stv"].iloc[:, 6:].columns)
    available_days = data["calendar"]["date"].iloc[:total_available_days]

    min_date = datetime.datetime.strptime(
        available_days.iloc[0], "%Y-%m-%d"
    ).astimezone()

    max_date = datetime.datetime.strptime(
        available_days.iloc[-1], "%Y-%m-%d"
    ).astimezone()

    start_date = left_column.date_input(
        "Start date",
        min_value=min_date,
        max_value=max_date,
        value=min_date,
        format="YYYY-MM-DD",
        key=key_s + "4",
    )

    end_date = left_column.date_input(
        "End date",
        min_value=min_date,
        max_value=max_date,
        value=max_date,
        format="YYYY-MM-DD",
        key=key_s + "5",
    )

    if len(filtered_stv) == 0:
        module.warning("No data available.")
        return

    stv_ = (
        filtered_stv
        if len(filtered_stv) < n
        else filtered_stv.sample(n=n, random_state=42)
    )
    stv_random = stv_.drop(["id", "dept_id", "cat_id", "store_id", "state_id"], axis=1)
    stv_random = stv_random.groupby("item_id").sum()
    stv_random.columns = stv_random.columns.map(
        lambda x: (min_date + datetime.timedelta(days=int(x[2:]) - 1)).date()
    )
    column_start_index = stv_random.columns.get_loc(start_date)
    column_end_index = stv_random.columns.get_loc(end_date)
    stv_random = stv_random.iloc[:, column_start_index:column_end_index]
    fig = px.imshow(
        stv_random,
        color_continuous_scale=px.colors.sequential.Turbo,
        title=f"Sales Heatmap of random {n} samples",
        labels={"x": "Days", "y": "Products", "color": "Sales"},
    )
    fig.update_yaxes(showticklabels=False)
    module.plotly_chart(fig, use_container_width=True)
