import streamlit as s
import matplotlib.pyplot as plt

from utils.data_loader import *
from utils.data_cleaner import *
from utils.item_analysis import *
from utils.category_analysis import *
from utils.prediction import *
from utils.stock_analysis import *
from utils.recommendations import *
from utils.visualization import *
from utils.cost_consumption import *

DATA_PATH = "data/COSTING LIST MOUNT ROAD BUHARI.xlsx"

s.set_page_config(page_title="Cost Analysis Dashboard",layout="wide")

raw_df = load_data(DATA_PATH)
df = clean_data(raw_df)

s.title("Restaurant Cost Analysis & Prediction")

s.header("Item Wise Cost Per Unit")

item_cost_df = calculate_cost_per_unit(df)

top_items = item_cost_df.head(10)
plt.figure()
plt.barh(top_items["item"],top_items["cost_per_unit"])
plt.xlabel("Cost Per Unit")
s.pyplot(plt)

s.header("Category-Wise Cost Distribution")
category_df = category_summary(df)

plt.figure()
plt.pie(category_df["total_cost"],labels=category_df["category"],autopct="%1.1f%%")
s.pyplot(plt)

s.header("Cost Prediction")
items = sorted(df["item"].unique())

selected_item = s.selectbox(
    label="Select Item (Type to Search)",
    options=items,
    index=None,
    placeholder="Start typing item name..."
)

if selected_item:
    item_df = df[df["item"] == selected_item]

    predictor = CostPrediction()
    predictor.train(item_df["quantity"], item_df["cost"])

    quantity_input = s.number_input(
        "Enter Quantity (KG / Units)",
        min_value=1.0,
        step=1.0
    )

    predicted_cost = predictor.predict(quantity_input)

    s.success(f"Estimated Cost: ₹ {predicted_cost:,.2f}")

s.header("Stock Analysis")

stock_df = estimate_daily_consumption(df)
stock_report = stock_status(stock_df)

s.dataframe(stock_report)

low_stock = stock_report[stock_report["low_stock_alert"]]

if not low_stock.empty:
    s.error("Low Stock Alert!")
    s.dataframe(low_stock)
else:
    s.success("All stock levels are healthy")


s.header("Cost & Consumption Analysis")

PLATES_PER_DAY = 300

ingredient_df = ingredient_consumption(df)
monthly_df = monthly_projection(df)
plate_cost = cost_per_plate(df, PLATES_PER_DAY)

s.metric("Cost per Plate (₹)", plate_cost)

s.subheader("Ingredient-wise Cost & Consumption")
s.dataframe(ingredient_df)

s.pyplot(cost_bar_chart(ingredient_df))
s.pyplot(cost_pie_chart(ingredient_df.head(8)))
s.pyplot(monthly_trend_chart(monthly_df))

# Recommendations
s.subheader("Cost Saving Suggestions")
reco = cost_saving_recommendations(ingredient_df)
s.dataframe(reco)