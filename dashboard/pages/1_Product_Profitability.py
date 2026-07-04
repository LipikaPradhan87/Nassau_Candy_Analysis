import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]

st.subheader("Top 10 Products by Gross Profit")

@st.cache_data
def load_data():
    return pd.read_csv(BASE_DIR / "data" / "cleaned" / "nassau_featured.csv")

df = load_data()

st.title("Product Profitability Analysis")
st.markdown("Analyze product sales, profit, margin, and performance.")


st.markdown("KPI Cards")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Products", df["Product Name"].nunique())
col2.metric("Total Sales", f"${df['Sales'].sum():,.0f}")
col3.metric("Total Gross Profit", f"${df['Gross Profit'].sum():,.0f}")

avg_margin = (df["Gross Profit"].sum() / df["Sales"].sum()) * 100
col4.metric("Average Gross Margin", f"{avg_margin:.2f}%")

#Top 10 Products by Gross profit
top_products = (
    df.groupby("Product Name", as_index=False)["Gross Profit"]
    .sum()
    .sort_values("Gross Profit", ascending=False)
    .head(10)
)
fig = px.bar(
    top_products,
    x="Gross Profit",
    y="Product Name",
    orientation="h",
    text_auto=True,
    title="Top 10 Products by Gross Profit",
    color_discrete_sequence=["#4CAF50"] 
)

fig.write_image(
    "../visuals/top_10_products_gross_profit.png",
    width=1200,
    height=700,
    scale=2
)

st.plotly_chart(fig)

#Top 10 Prdocts By sales

top_sales = (
    df.groupby("Product Name", as_index=False)["Sales"]
      .sum()
      .sort_values("Sales", ascending=False)
      .head(10)
)
fig = px.bar(
    top_sales,
    x="Sales",
    y="Product Name",
    orientation="h",
    text_auto=True,
    title="Top 10 Products by Sales"
)
st.plotly_chart(fig)

#Top 10 Products by Gross Margin %
df["Gross Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100

top_margin = (
    df.groupby("Product Name", as_index=False)["Gross Margin %"]
      .mean()
      .sort_values("Gross Margin %", ascending=False)
      .head(10)
)

fig = px.bar(
    top_margin,
    x="Gross Margin %",
    y="Product Name",
    orientation="h",
    text_auto=True,
    title="Top 10 Products by Gross Margin %"
)
st.plotly_chart(fig)

#Bottom 10 Products by Gross Profit
bottom_products = (
    df.groupby("Product Name", as_index=False)["Gross Profit"]
      .sum()
      .sort_values("Gross Profit")
      .head(10)
)

fig = px.bar(
    bottom_products,
    x="Gross Profit",
    y="Product Name",
    orientation="h",
    text_auto=True,
    title="Bottom 10 Products by Gross Profit"
)
st.plotly_chart(fig)

#Search Product

selected_product = st.selectbox(
    "Select Product",
    sorted(df["Product Name"].unique())
)

product_df = df[df["Product Name"] == selected_product]

st.subheader("Product Details")

col1, col2 = st.columns(2)

col1.metric(
    "Sales",
    f"${product_df['Sales'].sum():,.0f}"
)

col2.metric(
    "Gross Profit",
    f"${product_df['Gross Profit'].sum():,.0f}"
)

col1.metric(
    "Cost",
    f"${product_df['Cost'].sum():,.0f}"
)

col2.metric(
    "Units Sold",
    f"{product_df['Units'].sum():,.0f}"
)

margin = (
    product_df["Gross Profit"].sum()
    /
    product_df["Sales"].sum()
) * 100

st.metric(
    "Gross Margin %",
    f"{margin:.2f}%"
)

st.dataframe(product_df)

#Product Summary Table
st.markdown("Summary Table")
product_summary = (
    df.groupby("Product Name", as_index=False)
      .agg({
          "Sales": "sum",
          "Cost": "sum",
          "Gross Profit": "sum",
          "Units": "sum"
      })
)

product_summary["Gross Margin %"] = (
    product_summary["Gross Profit"] /
    product_summary["Sales"]
) * 100

st.dataframe(product_summary)


st.subheader("Key Insights")

st.markdown("""
- The top 10 products contribute a significant share of the total gross profit.
- Some products generate high sales but relatively low margins.
- Low-profit products should be reviewed for pricing or cost optimization.
""")