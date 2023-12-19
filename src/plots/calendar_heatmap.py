"""Calendar heatmap plot."""
from __future__ import annotations

from typing import TYPE_CHECKING

from pandas import DataFrame, Index, to_datetime
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
    d = 1400
    stv_ = data["stv"].sample(n=n, random_state=42)
    stv_random = stv_.drop(["item_id", "dept_id", "store_id", "state_id"], axis=1)
    stv_random = stv_random.groupby("cat_id").sum()
    stv_random = stv_random.iloc[:, 1 : d + 1]
    stv_random.columns = Index(data["calendar"]["date"].iloc[:d])
    stv_random = stv_random.T.reset_index()
    stv_random["date"] = to_datetime(stv_random["date"])
    fig = [
        calplot(stv_random, x="date", y=y, dark_theme=True, years_title=True, colorscale=c, gap=0, name="Sales", month_lines_width=3, month_lines_color="#fff").update_xaxes(
            tickangle=0
        )
        for y, c in [("FOODS", "greens"), ("HOBBIES", "blues"), ("HOUSEHOLD", "reds")]
    ]
    category = module.selectbox("Select category:", ["FOODS", "HOBBIES", "HOUSEHOLD"], key=key_s + "0")
    if category == "FOODS":
        module.plotly_chart(fig[0])
    if category == "HOBBIES":
        module.plotly_chart(fig[1])
    if category == "HOUSEHOLD":
        module.plotly_chart(fig[2])
