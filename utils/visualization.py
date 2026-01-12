import matplotlib.pyplot as plt
import pandas as pd


def cost_bar_chart(df: pd.DataFrame):
    top = df.head(10)
    plt.figure()
    plt.barh(top["item"], top["total_cost"])
    plt.xlabel("Total Cost (₹)")
    plt.tight_layout()
    return plt


def cost_pie_chart(df: pd.DataFrame):
    plt.figure()
    plt.pie(df["total_cost"], labels=df["item"], autopct="%1.1f%%")
    plt.tight_layout()
    return plt


def monthly_trend_chart(df: pd.DataFrame):
    top = df.head(5)
    plt.figure()
    plt.plot(top["item"], top["monthly_cost"], marker="o")
    plt.ylabel("Monthly Cost (₹)")
    plt.tight_layout()
    return plt
