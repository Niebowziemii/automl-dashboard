"""Products correlation plot."""
from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.express as px

if TYPE_CHECKING:
    from pandas import DataFrame
    from streamlit.delta_generator import DeltaGenerator


def plot(data: dict[str, DataFrame], module: DeltaGenerator, key_s: str) -> None:  # noqa: ARG001
    """SCorrelation of random sample of products.

    Args:
        data (dict[str, DataFrame]): M5 forecasting accuracy dict formatted as in load.py.
        module (DeltaGenerator): Layout element for rendering.
        key_s (str): Key for streamlit components.
    """
    n = 100
    stv_ = data["stv"].sample(n=n, random_state=42)
    stv_random = stv_.drop(["id", "dept_id", "cat_id", "store_id", "state_id"], axis=1)
    stv_random = stv_random.groupby("item_id").sum()
    stv_random = stv_random.iloc[:, 1:]
    corr = stv_random.T.corr()
    corr = corr.fillna(0)
    fig = px.imshow(
        corr, color_continuous_scale=px.colors.sequential.Turbo, title=f"Correlation between random {n} Products", labels={"x": "", "y": "", "color": "Correlation"}
    )
    fig.update_yaxes(showticklabels=False)
    fig.update_xaxes(showticklabels=False)
    module.plotly_chart(fig)
