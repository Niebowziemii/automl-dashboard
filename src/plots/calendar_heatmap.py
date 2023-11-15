"""Calendar heatmap plot"""
import pandas as pd
import plotly.express as px
from plotly_calplot import calplot
import streamlit as st

def plot(calendar, stv, ste, sp, ss):
    n = 100
    d = 1400
    stv_= stv.sample(n=n, random_state=42)
    stv_random = stv_.drop(["item_id","dept_id","store_id","state_id"], axis=1)
    stv_random = stv_random.groupby("cat_id").sum()
    # map column names to dates from calendar:
    stv_random = stv_random.iloc[:, 1:d + 1]
    stv_random.columns = calendar["date"][:d]
    stv_random = stv_random.T.reset_index()
    stv_random["date"] = pd.to_datetime(stv_random["date"])
    print(stv_random)
    # stv_random.index = stv_random.index.map(lambda x: f"ID_{x}")
    fig = [
        calplot(
            stv_random,
            x="date",
            y=y,
            dark_theme=True,
            years_title=True,
            colorscale=c,
            gap=0,
            name="Sales",
            month_lines_width=3,
            month_lines_color="#fff"
        ).update_xaxes(tickangle=0) for y, c in [("FOODS", "greens"), ("HOBBIES", "blues"), ("HOUSEHOLD", "reds")]
    ]
    tab1, tab2, tab3 = st.tabs(["FOODS", "HOBBIES", "HOUSEHOLD"])
    with tab1:
        st.plotly_chart(fig[0])
    with tab2:
        st.plotly_chart(fig[1])
    with tab3:
        st.plotly_chart(fig[2])