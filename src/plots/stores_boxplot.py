"""Stores boxplot."""
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
    """Sales per store per category of random n Samples.

    Args:
        data (dict[str, DataFrame]): M5 forecasting accuracy dict formatted as in load.py.
        module (DeltaGenerator): Layout element for rendering.
        key_s (str): Key for streamlit components.
    """
    left_column, rigth_column = module.columns(2)

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

    end_date = rigth_column.date_input(
        "End date",
        min_value=min_date,
        max_value=max_date,
        value=max_date,
        format="YYYY-MM-DD",
        key=key_s + "5",
    )
    n = 1000
    stv_ = data["stv"].sample(n=n, random_state=42)
    stv_random = stv_.drop(["id", "item_id", "dept_id", "state_id"], axis=1)
    stv_random = stv_random.melt(
        id_vars=["store_id", "cat_id"], var_name="date", value_name="sales"
    )
    stv_random = stv_random.groupby(["store_id", "cat_id", "date"]).sum().reset_index()
    stv_random["date"] = stv_random["date"].map(
        lambda x: (min_date + datetime.timedelta(days=int(x[2:]) - 1)).date()
    )
    stv_random = stv_random.loc[
        (stv_random["date"] >= start_date) & (stv_random["date"] <= end_date)
    ]
    fig = px.box(
        stv_random,
        x="store_id",
        y="sales",
        color="cat_id",
        title=f"Sales per store per category of random {n} samples",
        labels={"x": "Store", "y": "Sales in different days"},
    )
    module.plotly_chart(fig, use_container_width=True)
