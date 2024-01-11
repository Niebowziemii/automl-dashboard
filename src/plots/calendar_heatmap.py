"""Calendar heatmap plot."""
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, cast

from pandas import DataFrame
from plotly_calplot import calplot

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator


def plot(data: dict[str, DataFrame], module: DeltaGenerator, key_s: str) -> None:
    """Calendar plot with sales.

    Args:
        data (dict[str, DataFrame]): M5 forecasting accuracy dict formatted as in load.py.
        module (DeltaGenerator): Layout element for rendering.
        key_s (str): Key for streamlit components.
    """
    n = 100

    left_column, rigth_column = module.columns(2)

    available_states = list(data["stv"]["state_id"].unique())
    selected_states = left_column.multiselect("Select state:", available_states, available_states, key=key_s + "0")

    available_stores = list(
        filter(
            lambda store: store.startswith(tuple(selected_states)),
            list(data["stv"]["store_id"].unique()),
        )
    )
    selected_stores = rigth_column.multiselect("Select store:", available_stores, available_stores, key=key_s + "1")

    available_categories = list(data["stv"]["cat_id"].unique())
    selected_categories = left_column.multiselect("Select category:", available_categories, available_categories, key=key_s + "2")

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

    filtered_stv = data["stv"].query(f"state_id in {selected_states} & store_id in {selected_stores} & cat_id in {selected_categories} & dept_id in {selected_subcategories}")

    total_available_days = len(data["stv"].iloc[:, 6:].columns)
    available_days = data["calendar"]["date"].iloc[:total_available_days]

    min_date = datetime.datetime.strptime(available_days.iloc[0], "%Y-%m-%d").astimezone()

    max_date = datetime.datetime.strptime(available_days.iloc[-1], "%Y-%m-%d").astimezone()

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

    sample_stv = filtered_stv if len(filtered_stv) < n else filtered_stv.sample(n=n, random_state=42)

    stv_random = sample_stv.drop(["item_id", "dept_id", "store_id", "state_id"], axis=1)
    stv_random = stv_random.drop(columns=["cat_id"])
    stv_random = cast(DataFrame, stv_random.sum())
    stv_random = stv_random.iloc[1:].to_frame()  # type: ignore[operator]
    stv_random = stv_random.rename(columns={0: "sales"})
    stv_random["date"] = available_days.to_list()
    stv_random = stv_random.set_index("date")

    stv_between_dates = stv_random.loc[str(start_date) : str(end_date)]  # type: ignore[misc]
    stv_between_dates = stv_between_dates.reset_index()

    fig = calplot(
        stv_between_dates,
        x="date",
        y="sales",
        dark_theme=True,
        years_title=True,
        gap=0,
        name="Sales",
        month_lines_width=3,
        month_lines_color="#fff",
        colorscale="blues",
    ).update_xaxes(tickangle=0)

    module.plotly_chart(fig)
