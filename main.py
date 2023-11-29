from os import listdir
import streamlit as st
from importlib import import_module
from src.load import load_files
st.set_page_config(layout="wide")

data = load_files()
row_0 = st.columns(2)
row_1 = st.columns(2)

module_0_0 = row_0[0].selectbox("Select your plot", [None] + [plot[:-3] for plot in listdir("./src/plots") if plot not in ["__init__.py", "helper.py"]], key=0)
module_0_1 = row_0[1].selectbox("Select your plot", [None] + [plot[:-3] for plot in listdir("./src/plots") if plot not in ["__init__.py", "helper.py"]], key=1)
module_1_0 = row_1[0].selectbox("Select your plot", [None] + [plot[:-3] for plot in listdir("./src/plots") if plot not in ["__init__.py", "helper.py"]], key=2)
module_1_1 = row_1[1].selectbox("Select your plot", [None] + [plot[:-3] for plot in listdir("./src/plots") if plot not in ["__init__.py", "helper.py"]], key=3)


if module_0_0 is not None:
    selected_plot_module = import_module("src.plots." + module_0_0)
    selected_plot_module.plot(data, row_0[0])
if module_0_1 is not None:
    selected_plot_module = import_module("src.plots." + module_0_1)
    selected_plot_module.plot(data, row_0[1])
if module_1_0 is not None:
    selected_plot_module = import_module("src.plots." + module_1_0)
    selected_plot_module.plot(data, row_1[0])
if module_1_1 is not None:
    selected_plot_module = import_module("src.plots." + module_1_1)
    selected_plot_module.plot(data, row_1[1])
