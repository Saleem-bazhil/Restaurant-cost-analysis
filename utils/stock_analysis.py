import pandas as pd
from config.stock_config import (
    DAILY_PLATES_SOLD,
    SAFETY_DAYS,
    LEAD_TIME_DAYS,
    DEFAULT_OPENING_STOCK_KG
)


def estimate_daily_consumption(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estimate item-level daily consumption.
    Assumption: quantity column represents daily usage.
    """
    df = df.copy()

    # Aggregate consumption per item
    item_daily = (
        df.groupby("item", as_index=False)
        .agg(daily_consumption_kg=("quantity", "sum"))
    )

    return item_daily


def stock_status(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate stock status, alerts, and reorder quantity at ITEM level.
    """
    df = df.copy()

    # Assume same opening stock for all items (configurable)
    df["current_stock_kg"] = DEFAULT_OPENING_STOCK_KG

    # Days stock will last
    df["days_stock_left"] = (   
        df["current_stock_kg"] / df["daily_consumption_kg"]
    ).round(2)

    # Reorder level based on safety + lead time
    df["reorder_level"] = (
        df["daily_consumption_kg"] * (SAFETY_DAYS + LEAD_TIME_DAYS)
    ).round(2)

    # How much to reorder
    df["reorder_quantity"] = (
        df["reorder_level"] - df["current_stock_kg"]
    ).clip(lower=0).round(2)

    # Alert flag
    df["low_stock_alert"] = df["current_stock_kg"] <= df["reorder_level"]

    return df[[
        "item",
        "daily_consumption_kg",
        "current_stock_kg",
        "days_stock_left",
        "low_stock_alert",
        "reorder_quantity"
    ]]
