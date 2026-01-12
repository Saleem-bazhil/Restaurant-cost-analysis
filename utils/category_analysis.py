import pandas as p
from config.categories import CATEGORY_MAP

def assign_category(item:str) -> str:
    for key,category in CATEGORY_MAP.items():
        if key in item:
            return category
    return "others"

def category_summary(df:p.DataFrame) -> p.DataFrame:
    df = df.copy()
    df["category"] = df["item"].apply(assign_category)

    return(
        df.groupby("category",as_index=False)
        .agg(total_cost=("cost","sum"))
        .sort_values("total_cost",ascending=False)
    )