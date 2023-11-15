"""Sales heatmap plot"""
import plotly.express as px
import streamlit as st

def plot(calendar, stv, ste, sp, ss):
    n = 100
    d = 300
    stv_ = stv.sample(n=n, random_state=42)
    stv_random = stv_.drop(["id", "dept_id", "cat_id", "store_id", "state_id"], axis=1)
    stv_random = stv_random.groupby("item_id").sum()
    stv_random = stv_random.iloc[:, 1:d+1]
    # stv_random.index = stv_random.index.map(lambda x: f"ID_{x}")
    print(stv_random.iloc[0])
    fig = px.imshow(
        stv_random,
        color_continuous_scale=px.colors.sequential.Turbo,
        title=f"Sales Heatmap of random {n} Samples over {d} days",
        labels=dict(x="Days", y="Products", color="Sales")
    )
    fig.update_yaxes(showticklabels=False)
    st.plotly_chart(fig)
