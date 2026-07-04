import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]

st.title("Division Performance Analysis")
st.markdown("Compare sales, profit, cost and margin across product divisions.")

@st.cache_data
def load_data():
    return pd.read_csv(BASE_DIR / "data" / "cleaned" / "nassau_featured.csv")

df = load_data()

#Division Summary

division_summary = (
    df.groupby("Division", as_index=False).agg({
        "Sales": "sum",
        "Cost":"sum",
        "Gross Profit":"sum",
        "Units":"sum"
    })
)

division_summary["Gross Margin %"] =(
    division_summary["Gross Profit"]/division_summary["Sales"]
)*100

#KPI Cards
col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Total Divisions",
    division_summary["Division"].nunique()
)

col2.metric(
    "Total Sales",
    f"${division_summary['Sales'].sum():,.0f}"
)

col3.metric(
    "Total Profit",
    f"${division_summary['Gross Profit'].sum():,.0f}"
)

col4.metric(
    "Average Margin",
    f"{division_summary['Gross Margin %'].mean():.2f}%"
)

#Revenue by Division
fig = px.bar(
    division_summary,
    x="Division",
    y="Sales",
    text_auto=True,
    title="Revenue by Division"
)

st.plotly_chart(fig, use_container_width=True)

#Gross Profit by Division
fig = px.bar(
    division_summary,
    x="Division",
    y="Gross Profit",
    text_auto=True,
    title="Gross Profit by Division",
    color_discrete_sequence=["#2196F3"] 
)
fig.write_image(
    "../visuals/gross_profit_by_division.png",
    width=1200,
    height=700,
    scale=2
)

st.plotly_chart(fig, use_container_width=True)

#Cost by Division
fig = px.bar(
    division_summary,
    x="Division",
    y="Cost",
    text_auto=True,
    title="Cost by Division"
)

st.plotly_chart(fig, use_container_width=True)

#Gross Margin by Division
fig = px.bar(
    division_summary,
    x="Division",
    y="Gross Margin %",
    text_auto=".2f",
    title="Gross Margin (%) by Division"
)

st.plotly_chart(fig, use_container_width=True)

#Revenue vs Profit
compare = division_summary.melt(
    id_vars="Division",
    value_vars=["Sales","Gross Profit"],
    var_name="Metric",
    value_name="Amount"
)

fig = px.bar(
    compare,
    x="Division",
    y="Amount",
    color="Metric",
    barmode="group",
    text_auto=True,
    title="Revenue vs Gross Profit"
)

st.plotly_chart(fig, use_container_width=True)

#Division-wise Units Sold
fig = px.pie(
    division_summary,
    names="Division",
    values="Units",
    title="Units Sold by Division"
)

st.plotly_chart(fig, use_container_width=True)

#Division Summary Table
st.subheader("Division Summary")

st.dataframe(division_summary)

#Best Performing Division
best = division_summary.loc[
    division_summary["Gross Profit"].idxmax()
]

st.success(
    f"🏆 Best Performing Division: {best['Division']} "
    f"with Gross Profit of ${best['Gross Profit']:,.0f}"
)

#Lowest Performing Division
worst = division_summary.loc[
    division_summary["Gross Profit"].idxmin()
]

st.warning(
    f"⚠ Lowest Performing Division: {worst['Division']}"
)

st.subheader("Business Insights")

st.markdown("""
- Compare the sales contribution of each division.
- Evaluate whether higher sales also result in higher profits.
- Identify divisions with strong or weak gross margins.
- Use these insights to support pricing, marketing, and inventory decisions.
""")