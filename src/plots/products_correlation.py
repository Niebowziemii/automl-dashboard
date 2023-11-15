"""Products correlation plot"""
import plotly.express as px
import streamlit as st
import numpy as np

def plot(calendar, stv, ste, sp, ss):
    n = 100
    stv_ = stv.sample(n=n, random_state=42)
    stv_random = stv_.drop(["id", "dept_id", "cat_id", "store_id", "state_id"], axis=1)
    stv_random = stv_random.groupby("item_id").sum()
    stv_random = stv_random.iloc[:, 1:]
    corr = stv_random.T.corr()
    corr = corr.fillna(0)
    fig = px.imshow(
        corr,
        color_continuous_scale=px.colors.sequential.Turbo,
        title=f"Correlation between random {n} Products",
        labels=dict(x="", y="", color="Correlation")
    )
    fig.update_yaxes(showticklabels=False)
    fig.update_xaxes(showticklabels=False)
    st.plotly_chart(fig)