import pandas as pd


def ingredient_consumption(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("item", as_index=False)
        .agg(
            total_quantity=("quantity", "sum"),
            total_cost=("cost", "sum")
        )
    )

    summary["cost_per_unit"] = (
        summary["total_cost"] / summary["total_quantity"]
    ).round(2)

    summary["cost_pct"] = (
        summary["total_cost"] / summary["total_cost"].sum() * 100
    ).round(2)

    return summary.sort_values("total_cost", ascending=False)


def cost_per_plate(df: pd.DataFrame, plates_per_day: int) -> float:
    return round(df["cost"].sum() / plates_per_day, 2)


def monthly_projection(df: pd.DataFrame, days: int = 30) -> pd.DataFrame:
    return (
        df.groupby("item", as_index=False)
        .agg(
            monthly_quantity=("quantity", lambda x: x.sum() * days),
            monthly_cost=("cost", lambda x: x.sum() * days)
        )
        .sort_values("monthly_cost", ascending=False)
    )
