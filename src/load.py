"""Loading function."""
from __future__ import annotations

from pathlib import Path

import streamlit as st
from pandas import DataFrame, read_csv


@st.cache_data()
def load_files() -> dict[str, DataFrame]:
    """Function loading input data into RAM memory."""
    directory = "./input/m5-forecasting-accuracy"
    calendar = read_csv(Path(directory, "calendar.csv"))
    stv = read_csv(Path(directory, "sales_train_validation.csv"))
    ste = read_csv(Path(directory, "sales_train_evaluation.csv"))
    sp = read_csv(Path(directory, "sell_prices.csv"))
    ss = read_csv(Path(directory, "sample_submission.csv"))
    return {"calendar": calendar, "stv": stv, "ste": ste, "sp": sp, "ss": ss}
