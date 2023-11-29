"""Helper functions for data processing."""
from pandas import DataFrame


def helper_func(frame: DataFrame) -> DataFrame:
    """Preprocessing function."""
    frame = frame.drop(["item_id", "dept_id", "cat_id", "store_id", "state_id"], axis=1)
    frame = frame.melt(id_vars="id", var_name="dates", value_name="sales")
    frame["id"] = frame["id"].str.replace("_validation", "")
    return frame
