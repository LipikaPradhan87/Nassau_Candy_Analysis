import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


st.set_page_config(
    page_title="Nassau Candy Dashboard",
    page_icon="🍬",
    layout="wide"
)


st.title("Nassau Candy Distributor Dashboard")
st.markdown("### Product Line Profitability & Margin Performance Analysis")

@st.cache_data
def load_data():
    return pd.read_csv(BASE_DIR / "data" / "cleaned" / "nassau_featured.csv")

df = load_data()
st.write(df.head())

#Sidebar Filters
st.sidebar.header("Filters")

st.markdown('Filter Table Data')
division = st.sidebar.multiselect(
    "Select Division",
    options = df["Division"].unique(),
    default=df["Division"].unique()
)

region = st.sidebar.multiselect(
    "Select Region",
    options = df["Region"].unique(),
    default=df["Region"].unique()
)

#filter data
filtered_df = df[
    (df["Division"].isin(division)) &
    (df["Region"].isin(region))
]

st.write(filtered_df.head())

#Display KPI Cards
st.markdown("KPI Cards")
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${filtered_df['Sales'].sum():,.0f}"
)

col2.metric(
    "Total Profit",
    f"${filtered_df['Gross Profit'].sum():,.0f}"
)

col3.metric(
    "Total Cost",
    f"${filtered_df['Cost'].sum():,.0f}"
)

margin = (
    filtered_df["Gross Profit"].sum()
    / filtered_df["Sales"].sum()
) * 100

col4.metric(
    "Gross Margin %",
    f"{margin:.2f}%"
)

#Sales by Division
division_sales = (
    filtered_df
    .groupby("Division")["Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    division_sales,
    x="Division",
    y="Sales",
    text_auto=".2s",
    title="Sales by Division"
)

st.plotly_chart(fig, use_container_width=True)

#Gross Profit by Division
division_profit = (
    filtered_df
    .groupby("Division")["Gross Profit"]
    .sum()
    .reset_index()
)

fig = px.bar(
    division_profit,
    x="Division",
    y="Gross Profit",
    text_auto=".2s",
    title="Gross Profit by Division"
)

st.plotly_chart(fig, use_container_width=True)


#Cost vs Sales Scatter Plot
fig = px.scatter(
    filtered_df,
    x="Cost",
    y="Sales",
    color="Division",
    hover_data=["Product Name"],
    title="Cost vs Sales"
)

st.plotly_chart(fig, use_container_width=True)

#Top 10 Products by Profit
top_products = (
    filtered_df
    .groupby("Product Name")["Gross Profit"]
    .sum()
    .nlargest(10)
    .reset_index()
)

fig = px.bar(
    top_products,
    x="Gross Profit",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Gross Profit"
)

st.plotly_chart(fig, use_container_width=True)

#Show Filtered Data
st.subheader("Filtered Dataset")

st.dataframe(filtered_df)

#Add Download Button
st.download_button(
    label="Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("Created by Lipika Pradhan | Nassau Candy Profitability Dashboard")