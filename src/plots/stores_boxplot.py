"""Stores boxplot"""
import plotly.express as px
import streamlit as st

def plot(calendar, stv, ste, sp, ss):
    n = 100
    stv_ = stv.sample(n=n, random_state=42)
    stv_random = stv_.drop(["id", "item_id","dept_id", "state_id"], axis=1)
    stv_random = stv_random.melt(id_vars=["store_id", "cat_id"], var_name="date", value_name="sales")
    stv_random = stv_random.groupby(["store_id", "cat_id", "date"]).sum().reset_index()
    fig = px.box(
        stv_random,
        x="store_id",
        y="sales",
        color="cat_id",
        title=f"Sales per store per category of random {n} Samples",
        labels=dict(x="Store", y="Sales in different days")
    )
    st.plotly_chart(fig)
