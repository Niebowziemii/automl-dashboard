"""Helper functions for data processing."""
def helper_func(df):
    df = df.drop(["item_id","dept_id","cat_id","store_id","state_id"], axis=1)
    df = df.melt(id_vars="id",var_name='dates',value_name="sales" )
    df["id"] = df["id"].str.replace('_validation', '')
    return df