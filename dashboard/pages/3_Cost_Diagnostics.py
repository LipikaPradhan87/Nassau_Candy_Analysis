import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]

st.title("Cost Diagnostics")
st.markdown("Analyze product cost efficiency and identify margin risks.")

@st.cache_data
def load_data():
    return pd.read_csv(BASE_DIR / "data" / "cleaned" / "nassau_featured.csv")

df = load_data()


# Create Gross Margin %
df["Gross Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100

#KPI Cards
col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Total Cost",
    f"${df['Cost'].sum():,.0f}"
)
col2.metric(
    "Average Cost",
    f"${df['Cost'].mean():,.2f}"
)

highest = df.loc[df["Cost"].idxmax()]
lowest = df.loc[df["Cost"].idxmin()]

col3.metric(
    "Highest Cost",
    f"${highest['Cost']:,.0f}"
)

col3.caption(f"Product: {highest['Product Name']}")

col4.metric(
    "Lowest Cost Product",
    f"${lowest['Cost']:,.0f}"
)
col4.caption(f"Product: {lowest['Product Name']}")

#Cost vs Sales Scatter Plot
st.subheader("Cost vs Sales")

fig = px.scatter(
    df,
    x = "Cost",
    y = "Sales",
    color="Division",
    hover_name="Product Name",
    title="Cost vs Sales",
    color_discrete_sequence=[
        "#FF9800",
        "#2196F3",
        "#4CAF50",
        "#E91E63",
        "#9C27B0",
        "#795548"
    ]
)
fig.write_image(
    "../visuals/cost_vs_sales.png",
    width=1200,
    height=700,
    scale=2
)

st.plotly_chart(fig, use_container_width=True)

#Cost vs Gross Profit
st.subheader('Cost vs Gross Profit')

fig = px.scatter(
    df,
    x = "Cost",
    y = "Gross Profit",
    color = "Division",
    hover_name= "Product Name",
    title = "Cost vs Gross Profit"
)

st.plotly_chart(fig, use_container_width=True)

#Cost Distribution
st.subheader("Cost Distribution")

fig = px.histogram(
    df,
    x = "Cost",
    nbins=30,
    title="Distribution of Product Costs"
)

st.plotly_chart(fig, use_container_width=True)

#High Cost Products

st.subheader("Top 10 Highest Cost Products")
high_cost = (
    df.groupby("Product Name", as_index=False)
    .agg({
        "Cost":"sum",
        "Sales":"sum",
        "Gross Profit": "sum"
    })
    .sort_values("Cost", ascending=False)
    .head(10)
)

fig = px.bar(
    high_cost,
    x = "Cost",
    y = "Product Name",
    orientation="h",
    text_auto=True,
    title="Top 10 Highest Cost Products"
)

st.plotly_chart(fig, use_container_width=True)

#Products with margins below 15%.

st.subheader("Margin Risk Products")
risk_products = df[df["Gross Margin %"] < 15]
st.dataframe(
    risk_products[
        [
            "Product Name",
            "Sales",
            "Cost",
            "Gross Profit",
            "Gross Margin %"
        ]
    ]
)

#Product Search
selected = st.selectbox(
    "Select Product",
    sorted(df["Product Name"].unique())
)

product = df[df["Product Name"] == selected]

st.write(product)

st.subheader("Business Recommendations")

st.markdown("""
- Review products with low gross margins.
- Renegotiate supplier or manufacturing costs for high-cost items.
- Evaluate pricing strategies for products with high sales but low profit.
- Consider discontinuing consistently low-performing products after further business review.
""")