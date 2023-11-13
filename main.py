from os import listdir
import streamlit as st
from importlib import import_module
from src.load import load_files

module = st.selectbox("Select your plot", [None] + [plot[:-3] for plot in listdir("./src/plots") if plot not in ["__init__.py", "helper.py"]])
if module is not None:
    selected_plot_module = import_module("src.plots." + module)

    selected_plot_module.plot(*load_files())


