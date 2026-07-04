import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]

st.title("Regional Performance Analysis")

st.markdown("""
Analyze sales, profit and margin across Regions, States and Cities.
""")

@st.cache_data
def load_data():
    return pd.read_csv(BASE_DIR / "data" / "cleaned" / "nassau_featured.csv")

df = load_data()

df["Gross Margin %"] = (
    df["Gross Profit"] /
    df["Sales"]
) * 100

#Regional Summary
region_summary = (
    df.groupby("Region", as_index=False)
      .agg({
          "Sales":"sum",
          "Gross Profit":"sum",
          "Cost":"sum",
          "Units":"sum"
      })
)

region_summary["Gross Margin %"] = (
    region_summary["Gross Profit"] /
    region_summary["Sales"]
) * 100

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Regions",
    region_summary["Region"].nunique()
)

col2.metric(
    "Highest Sales Region",
    region_summary.loc[
        region_summary["Sales"].idxmax(),
        "Region"
    ]
)

col3.metric(
    "Highest Profit Region",
    region_summary.loc[
        region_summary["Gross Profit"].idxmax(),
        "Region"
    ]
)

col4.metric(
    "Average Margin",
    f"{region_summary['Gross Margin %'].mean():.2f}%"
)

#Sales By Region
fig = px.bar(
    region_summary,
    x="Region",
    y="Sales",
    text_auto=True,
    title="Sales by Region"
)

st.plotly_chart(fig, use_container_width=True)

#Profit by Region
fig = px.bar(
    region_summary,
    x="Region",
    y="Gross Profit",
    text_auto=True,
    title="Gross Profit by Region"
)

st.plotly_chart(fig, use_container_width=True)

#Gross Margin by region
fig = px.bar(
    region_summary,
    x="Region",
    y="Gross Margin %",
    text_auto=".2f",
    title="Gross Margin (%) by Region"
)

st.plotly_chart(fig, use_container_width=True)

#Revenue Vs Profit
compare = region_summary.melt(
    id_vars="Region",
    value_vars=["Sales","Gross Profit"],
    var_name="Metric",
    value_name="Amount"
)

fig = px.bar(
    compare,
    x="Region",
    y="Amount",
    color="Metric",
    barmode="group",
    text_auto=True,
    title="Revenue vs Gross Profit"
)

st.plotly_chart(fig, use_container_width=True)

#Sales By State
state_sales = (
    df.groupby("State/Province", as_index=False)["Sales"]
      .sum()
      .sort_values("Sales", ascending=False)
)

fig = px.bar(
    state_sales.head(10),
    x="Sales",
    y="State/Province",
    orientation="h",
    text_auto=True,
    title="Top 10 States by Sales"
)

st.plotly_chart(fig, use_container_width=True)

#Profit By state
state_profit = (
    df.groupby("State/Province", as_index=False)["Gross Profit"]
      .sum()
      .sort_values("Gross Profit", ascending=False)
)

fig = px.bar(
    state_profit.head(10),
    x="Gross Profit",
    y="State/Province",
    orientation="h",
    text_auto=True,
    title="Top 10 States by Gross Profit"
)

st.plotly_chart(fig, use_container_width=True)

#Top cities
city_sales = (
    df.groupby("City", as_index=False)["Sales"]
      .sum()
      .sort_values("Sales", ascending=False)
)

fig = px.bar(
    city_sales.head(10),
    x="Sales",
    y="City",
    orientation="h",
    text_auto=True,
    title="Top 10 Cities by Sales"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Regional Summary")

st.dataframe(region_summary)

best_region = region_summary.loc[
    region_summary["Gross Profit"].idxmax(),
    "Region"
]

lowest_region = region_summary.loc[
    region_summary["Gross Profit"].idxmin(),
    "Region"
]

st.subheader("Business Insights")

st.success(f"🏆 Best Performing Region: {best_region}")

st.warning(f"⚠ Lowest Performing Region: {lowest_region}")

st.markdown("""
- Regions with high sales and high margins are key growth areas.
- High-sales but low-margin regions should be reviewed for pricing and operating costs.
- Top-performing states and cities can guide future marketing and inventory planning.
""")