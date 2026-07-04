import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.title("Pareto Analysis")
st.markdown("Identify the products contributing the most to overall gross profit using the Pareto (80/20) principle.")

@st.cache_data
def load_data():
    return pd.read_csv("../data/cleaned/nassau_featured.csv")

df = load_data()

# Prepare Pareto Data
pareto = (
    df.groupby("Product Name", as_index=False)["Gross Profit"]
    .sum()
    .sort_values("Gross Profit", ascending=False)
)

pareto["Cum Profit"] = pareto["Gross Profit"].cumsum()

pareto["Cum Profit %"] = (
    pareto["Cum Profit"]/pareto["Gross Profit"].sum()
)*100

# Revenue Pareto
pareto_revenue = (
    df.groupby("Product Name", as_index=False)["Sales"]
      .sum()
      .sort_values("Sales", ascending=False)
)

pareto_revenue["Cum Revenue"] = pareto_revenue["Sales"].cumsum()

pareto_revenue["Cum Revenue %"] = (
    pareto_revenue["Cum Revenue"]
    / pareto_revenue["Sales"].sum()
) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Products",
    pareto["Product Name"].nunique()
)

col2.metric(
    "Total Gross Profit",
    f"${pareto['Gross Profit'].sum():,.0f}"
)

products_80 = (pareto["Cum Profit %"] <= 80).sum()

col3.metric(
    "Products for 80% Profit",
    products_80
)
products_80_revenue = (pareto_revenue["Cum Revenue %"] <= 80).sum()

col4.metric(
    "Products for 80% Revenue",
    products_80_revenue
)

#Pareto Chart
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=pareto["Product Name"],
        y=pareto["Gross Profit"],
        name="Gross Profit"
    )
)

fig.add_trace(
    go.Scatter(
        x=pareto["Product Name"],
        y=pareto["Cum Profit %"],
        mode="lines+markers",
        name="Cumulative Profit %",
        text=[f"{x:.1f}%" for x in pareto["Cum Profit %"]],
        yaxis="y2"
    )
)

fig.update_layout(
    title="Pareto Analysis of Gross Profit",
    xaxis_title="Product",
    yaxis_title="Gross Profit",
    yaxis2=dict(
        title="Cumulative Profit %",
        overlaying="y",
        side="right",
        range=[0,110]
    )
)

st.plotly_chart(fig, use_container_width=True)

#80% Threshold Table
st.subheader("Products Contributing to 80% of Gross Profit")

top_80 = pareto[pareto["Cum Profit %"] <= 80]

st.dataframe(top_80)

#Bottom 10 Products 
st.subheader("Lowest Profit Products")

bottom = pareto.tail(10)

fig = px.bar(
    bottom,
    x="Gross Profit",
    y="Product Name",
    orientation="h",
    text_auto=True,
    title="Bottom 10 Products by Gross Profit"
)

st.plotly_chart(fig, use_container_width=True)

#search Product
selected = st.selectbox(
    "Select Product",
    pareto["Product Name"]
)

details = df[df["Product Name"] == selected]

st.dataframe(details)

#Revenue Pareto chart
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=pareto_revenue["Product Name"],
        y=pareto_revenue["Sales"],
        name="Revenue"
    )
)

fig.add_trace(
    go.Scatter(
        x=pareto_revenue["Product Name"],
        y=pareto_revenue["Cum Revenue %"],
        mode="lines+markers",
        name="Cumulative Revenue %",
        text=[f"{x:.1f}%" for x in pareto_revenue["Cum Revenue %"]],
        yaxis="y2"
    )
)

fig.update_layout(
    title="Pareto Analysis of Revenue",
    xaxis_title="Product Name",
    yaxis_title="Revenue",
    yaxis2=dict(
        title="Cumulative Revenue %",
        overlaying="y",
        side="right",
        range=[0,110]
    )
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Key Insights")

st.markdown("""
- A small percentage of products contribute the majority of the company's gross profit.
- These products should receive priority in inventory planning and marketing campaigns.
- Products with consistently low profit should be reviewed for pricing, cost reduction, or discontinuation.
""")