import pandas as p

def calculate_cost_per_unit(df:p.DataFrame) -> p.DataFrame:
    df = df.copy()
    df["cost_per_unit"] = df["cost"] / df["quantity"]

    return(
        df.groupby(["item","unit"], as_index = False)
        .agg(
            total_quantity = ("quantity","sum"),
            total_cost = ("cost","sum"),
            cost_per_unit = ("cost_per_unit","mean")
        )
        .sort_values("cost_per_unit",ascending=False)
    )