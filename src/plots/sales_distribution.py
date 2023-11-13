"""Sales distribution plot"""
from src.plots.helper import helper_func
import pandas as pd
import plotly.express as px

def plot(calendar, stv, ste, sp, ss):
    n = 100
    stv_= stv.sample(n=n, random_state=42)

    stv_random = helper_func(stv_)

    merged = stv_random.merge(calendar, how="left", left_on="dates", right_on="d")

    merged_ = pd.DataFrame(merged.groupby("date")["sales"].sum()).reset_index()

    fig = px.line(merged_, x="date", y="sales", title=f'Sales Distribution of random {n} Samples', color_discrete_map= dict(color="red"))
    fig.show()