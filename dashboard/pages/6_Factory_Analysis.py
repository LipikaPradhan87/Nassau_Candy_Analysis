import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]

st.title("Factory Performance Analysis")

st.markdown("""
Analyze the performance of each manufacturing factory based on
Sales, Cost, Gross Profit and Margin.
""")

@st.cache_data
def load_data():
    return pd.read_csv(BASE_DIR / "data" / "cleaned" / "nassau_featured.csv")

df = load_data()

factory_map = {
    "Wonka Bar - Nutty Crunch Surprise":"Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows":"Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious":"Lot's O' Nuts",

    "Wonka Bar - Milk Chocolate":"Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel":"Wicked Choccy's",

    "Laffy Taffy":"Sugar Shack",
    "SweeTARTS":"Sugar Shack",
    "Nerds":"Sugar Shack",
    "Fun Dip":"Sugar Shack",
    "Fizzy Lifting Drinks":"Sugar Shack",

    "Everlasting Gobstopper":"Secret Factory",
    "Lickable Wallpaper":"Secret Factory",
    "Wonka Gum":"Secret Factory",

    "Hair Toffee":"The Other Factory",
    "Kazookles":"The Other Factory"
}

df["Factory"] = df["Product Name"].map(factory_map)

df["Gross Margin %"] = (
    df["Gross Profit"] /
    df["Sales"]
) * 100

factory_summary = (
    df.groupby("Factory", as_index=False)
      .agg({
          "Sales":"sum",
          "Cost":"sum",
          "Gross Profit":"sum",
          "Units":"sum"
      })
)

factory_summary["Gross Margin %"] = (
    factory_summary["Gross Profit"]
    /
    factory_summary["Sales"]
) * 100

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Factories",
    factory_summary["Factory"].nunique()
)

col2.write("**Highest Sales Factory**")
col2.success(
    factory_summary.loc[
        factory_summary["Sales"].idxmax(),
        "Factory"
    ]
)

col3.write("**Highest Profit Factory**")
col3.success(
    factory_summary.loc[
        factory_summary["Gross Profit"].idxmax(),
        "Factory"
    ]
)

col4.metric(
    "Average Margin",
    f"{factory_summary['Gross Margin %'].mean():.2f}%"
)

fig = px.bar(
    factory_summary,
    x="Factory",
    y="Sales",
    text_auto=True,
    title="Sales by Factory",
    color_discrete_sequence=["#9C27B0"] 
)
fig.write_image(
    "../visuals/sales_by_factory.png",
    width=1200,
    height=700,
    scale=2
)

st.plotly_chart(fig, use_container_width=True)

fig = px.bar(
    factory_summary,
    x="Factory",
    y="Gross Profit",
    text_auto=True,
    title="Gross Profit by Factory",
    color_discrete_sequence=["#4CAF50"] 
)
fig.write_image(
    "../visuals/gross_profit_by_factory.png",
    width=1200,
    height=700,
    scale=2
)

st.plotly_chart(fig, use_container_width=True)

fig = px.bar(
    factory_summary,
    x="Factory",
    y="Cost",
    text_auto=True,
    title="Manufacturing Cost by Factory"
)

st.plotly_chart(fig, use_container_width=True)

fig = px.bar(
    factory_summary,
    x="Factory",
    y="Gross Margin %",
    text_auto=".2f",
    title="Gross Margin (%) by Factory"
)

st.plotly_chart(fig, use_container_width=True)

compare = factory_summary.melt(
    id_vars="Factory",
    value_vars=["Sales","Gross Profit"],
    var_name="Metric",
    value_name="Amount"
)

fig = px.bar(
    compare,
    x="Factory",
    y="Amount",
    color="Metric",
    barmode="group",
    text_auto=True,
    title="Revenue vs Gross Profit"
)

st.plotly_chart(fig, use_container_width=True)

factory_location = pd.DataFrame({
    "Factory":[
        "Lot's O' Nuts",
        "Wicked Choccy's",
        "Sugar Shack",
        "Secret Factory",
        "The Other Factory"
    ],
    "Latitude":[
        32.881893,
        32.076176,
        48.119140,
        41.446333,
        35.117500
    ],
    "Longitude":[
        -111.768036,
        -81.088371,
        -96.181150,
        -90.565487,
        -89.971107
    ]
})

factory_map_df = factory_summary.merge(
    factory_location,
    on="Factory"
)

fig = px.scatter_map(
    factory_map_df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Factory",
    hover_data=["Sales", "Gross Profit"],
    size="Gross Profit",
    zoom=3,
    title="Factory Locations"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Factory Summary")

st.dataframe(factory_summary)

best_factory = factory_summary.loc[
    factory_summary["Gross Profit"].idxmax(),
    "Factory"
]

worst_factory = factory_summary.loc[
    factory_summary["Gross Profit"].idxmin(),
    "Factory"
]

st.subheader("Business Insights")

st.success(
    f"🏆 Best Performing Factory: {best_factory}"
)

st.warning(
    f"⚠ Lowest Performing Factory: {worst_factory}"
)

st.markdown("""
- Compare factory efficiency using sales, cost, and gross profit.
- Identify factories with high manufacturing costs but lower profit.
- Use these insights to improve production planning and optimize manufacturing resources.
""")