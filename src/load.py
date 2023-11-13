"""Loading function."""
import pandas as pd
from os import path
import streamlit as st

@st.cache_data()
def load_files():
    DIR = f"./input/m5-forecasting-accuracy"
    calendar = pd.read_csv(path.join(DIR, "calendar.csv"))
    stv = pd.read_csv(path.join(DIR, "sales_train_validation.csv"))
    ste = pd.read_csv(path.join(DIR, "sales_train_evaluation.csv"))
    sp = pd.read_csv(path.join(DIR, "sell_prices.csv"))
    ss = pd.read_csv(path.join(DIR, "sample_submission.csv"))
    return calendar, stv, ste, sp, ss