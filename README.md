# 🍬 Product Line Profitability & Margin Performance Analysis

## Project Overview

This project analyzes the profitability and margin performance of Nassau Candy Distributor using Python and Streamlit. The objective is to identify the products, divisions, regions, and factories that contribute the most to the company's profitability while highlighting areas that require cost optimization and pricing improvements.

The project includes data cleaning, feature engineering, exploratory data analysis (EDA), interactive dashboards, and business recommendations.

---

## Objectives

- Analyze product-level profitability.
- Calculate Gross Margin (%), Profit per Unit, Revenue Contribution, and Profit Contribution.
- Compare sales and profit across product divisions.
- Identify high-profit and low-margin products.
- Perform Pareto (80/20) Analysis.
- Analyze regional sales performance.
- Evaluate factory-wise profitability.
- Develop an interactive Streamlit dashboard for business insights.

---

## Project Structure

```
Nassau_Candy_Analysis/
│
├── app.py
├── data/
│   ├── raw/
│   └── cleaned/
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   └── 02_feature_engineering.ipynb
│   └── 03_eda.ipynb
│   └── 04_prfitability_analysis.ipynb
│   └── 05_pareto_analysis.ipynb

│
├── pages/
│   ├── 1_Product_Profitability.py
│   ├── 2_Division_Performance.py
│   ├── 3_Cost_Diagnostics.py
│   ├── 4_Pareto_Analysis.py
│   ├── 5_Regional_Analysis.py
│   └── 6_Factory_Analysis.py
│
├── reports/
│   ├── research_paper.docx
│   └── executive_summary.pdf
│
├── visuals/
    |___cost_vs_sales.png
    |___gross_profit_by_division.png
    |___gross_profit_by_factory.png
    |___gross_profit.png
    |___pareto_analysis.png
    |___sales_by_factory.png
    |___sales_distribution.png
    |___sales_division.png
    |___sales_region.png
    |___top_10_products_gross_profit.png

│
├── requirements.txt
└── README.md
```

---

## Dataset

The dataset contains sales transactions for Nassau Candy Distributor.

### Main Fields

- Order Date
- Ship Date
- Division
- Product Name
- Sales
- Cost
- Gross Profit
- Units
- Region
- State
- City

---

## Tools & Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Jupyter Notebook
- Visual Studio Code

---

## Key Features

### Product Profitability

- Top 10 Products by Gross Profit
- Top 10 Products by Sales
- Top 10 Products by Gross Margin
- Bottom 10 Products by Profit
- Product Summary

### Division Performance

- Sales by Division
- Gross Profit by Division
- Average Margin by Division

### Cost Diagnostics

- Cost vs Sales Scatter Plot
- Cost Distribution
- High Cost Products

### Pareto Analysis

- Revenue Pareto Chart
- Profit Pareto Chart
- 80% Revenue Contribution
- 80% Profit Contribution

### Regional Analysis

- Sales by Region
- Profit by Region
- Top Performing Regions

### Factory Analysis

- Factory-wise Sales
- Factory-wise Profit
- Factory Margin Comparison

---

## KPIs

- Total Sales
- Total Gross Profit
- Gross Margin %
- Profit per Unit
- Revenue Contribution
- Profit Contribution
- Total Products
- Total Divisions
- Total Factories

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Navigate to the Project

```bash
cd Nassau_Candy_Analysis
```

### 3. Create a Virtual Environment

```bash
python -m venv myvenv
```

### 4. Activate the Virtual Environment

**Windows**

```bash
myvenv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Streamlit Dashboard

```bash
streamlit run app.py
```

---

## Reports

This project includes:

- Research Paper
- Executive Summary
- Interactive Streamlit Dashboard

---

## Dashboard

The dashboard contains six interactive pages:

- Product Profitability
- Division Performance
- Cost Diagnostics
- Pareto Analysis
- Regional Analysis
- Factory Analysis

---

## Business Insights

The analysis helps identify:

- High-profit products
- Low-margin products
- Best-performing divisions
- Cost-intensive products
- Revenue concentration
- High-performing regions
- Efficient manufacturing factories

---

## Future Enhancements

- Sales Forecasting
- Demand Forecasting
- Machine Learning Models
- Inventory Optimization
- Real-time Database Integration
- Customer Segmentation
- Predictive Analytics

---

## Author

**Sonali**

Data Analytics Project

Unified Mentor Internship

---

##  License

This project is developed for educational and internship purposes.