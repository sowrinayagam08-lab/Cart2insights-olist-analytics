# 🛒 Cart2Insights – Decoding E-Commerce Performance

### Turning Raw E-Commerce Data into Meaningful Business Insights

An end-to-end **Data Analytics Project** using the Brazilian Olist E-Commerce Dataset, combining Python, SQL, statistical analysis, and interactive data visualization to understand business performance and customer behaviour.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" />
</p>

---

## 📌 Project Overview

**Cart2Insights** is an end-to-end e-commerce analytics project built using the Olist Brazilian E-Commerce dataset.

The project focuses on transforming raw transactional data into meaningful business insights through data cleaning, database management, SQL analysis, Python-based exploration, statistical testing, and interactive dashboard development.

Instead of simply analysing sales numbers, this project explores the complete e-commerce business journey — from customer purchases and seller performance to product categories, delivery operations, and customer satisfaction.

### 🎯 Business Objectives

The project aims to answer important business questions:

- How is the business performing in terms of revenue and orders?
- Which product categories generate the highest sales?
- Who are the top-performing sellers?
- How do customers behave, and how many return for repeat purchases?
- Are orders being delivered on time?
- Does delivery performance influence customer satisfaction?
- Are there statistically significant differences in customer reviews and business performance?

---

## 🧰 Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Database | MySQL |
| Database Management | MySQL Workbench |
| Data Manipulation | Pandas, NumPy |
| Data Visualization | Matplotlib, Seaborn, Plotly |
| Statistical Analysis | SciPy (T-Test, ANOVA, Chi-Square) |
| Dashboard Development | Streamlit |
| Development Environment | Jupyter Notebook, VS Code |
| Version Control | Git, GitHub |

---

## 📂 Dataset Description

This project uses the **Olist Brazilian E-Commerce Dataset**, which consists of 9 interconnected datasets.

| No. | Dataset | Description |
|---|---|---|
| 1 | Customers | Customer IDs, locations, and unique customer information |
| 2 | Geolocation | Brazilian postal codes, latitude, longitude, city, and state |
| 3 | Order Items | Products purchased, sellers, prices, and freight values |
| 4 | Order Payments | Payment methods, installments, and payment values |
| 5 | Order Reviews | Customer ratings, review comments, and timestamps |
| 6 | Orders | Order status and purchase, approval, and delivery timestamps |
| 7 | Products | Product details, dimensions, weight, and category |
| 8 | Sellers | Seller IDs and location information |
| 9 | Product Category Translation | Portuguese-to-English product category mapping |

All 9 datasets were cleaned and prepared before being stored in MySQL.

---

## 🔄 End-to-End Project Workflow

The project follows a structured data analytics pipeline:

```text
        RAW OLIST DATA
              |
              ▼
      DATA UNDERSTANDING
              |
              ▼
       DATA QUALITY CHECK
              |
              ▼
       DATA CLEANING
       (9 CSV DATASETS)
              |
              ▼
       DATABASE DESIGN
        (ER DIAGRAM)
              |
              ▼
       MYSQL DATABASE
      (PK & FK CONSTRAINTS)
              |
              ▼
         SQL ANALYSIS
   (Joins, CTEs, Windows)
              |
              ▼
     PYTHON CONNECTION
        (JUPYTER)
              |
              ▼
     FEATURE ENGINEERING
              |
              ▼
       EXPLORATORY DATA
          ANALYSIS
              |
              ▼
     STATISTICAL ANALYSIS
   (T-Test, ANOVA, Chi-Square)
              |
              ▼
     STREAMLIT DASHBOARD
              |
              ▼
       BUSINESS INSIGHTS
```

### 1️⃣ Data Cleaning & Preprocessing

- Imported all 9 raw CSV datasets using Pandas.
- Inspected dataset shapes, columns, and data types.
- Identified missing values and duplicate records.
- Handled inconsistent text values and categorical data.
- Standardized city names and other relevant fields.
- Converted date columns into appropriate datetime formats.
- Checked primary key uniqueness and data consistency.
- Prepared cleaned datasets for database loading.

### 2️⃣ Database Design & Management

Designed a relational MySQL database to organize the cleaned e-commerce datasets.

**Key activities:**
- Created the MySQL database.
- Designed tables based on the Entity Relationship (ER) Diagram.
- Imported cleaned CSV files into MySQL.
- Implemented Primary Key (PK) and Foreign Key (FK) constraints.
- Established relationships between the 9 tables.
- Verified row counts and table relationships after loading.

### 3️⃣ SQL Analysis

Used SQL to retrieve, combine, and analyse business information.

**SQL concepts applied:**

- SELECT, WHERE, ORDER BY
- GROUP BY and HAVING
- Aggregate Functions
- INNER JOIN, LEFT JOIN
- Subqueries
- Common Table Expressions (CTEs)
- Window Functions
- LAG() and ranking functions

**Business analysis included:**
- Revenue and order performance.
- Customer purchasing behaviour.
- Seller revenue and performance.
- Product category analysis.
- Payment method distribution.
- Delivery performance and delays.
- Customer review analysis.

### 4️⃣ Python & MySQL Integration

Connected the MySQL database with Python using SQLAlchemy.

Used Jupyter Notebook to retrieve SQL data into Pandas DataFrames for further analysis.

This integration created a smooth workflow between database querying, data manipulation, visualization, and statistical analysis.

### 5️⃣ Feature Engineering

Created additional business-related features to gain deeper insights.

| Feature | Purpose |
|---|---|
| Total Order Value | Understand the monetary value of orders |
| Delivery Days | Measure the time taken to deliver orders |
| Delivery Delay | Identify delayed deliveries |
| Customer Order Count | Measure customer purchase frequency |
| Customer Total Spending | Understand customer spending behaviour |
| Average Order Value | Measure average transaction value |
| Seller Revenue | Evaluate seller contribution |
| Seller Order Count | Measure seller order volume |
| Repeat Customer Indicator | Identify customers with multiple orders |

### 6️⃣ Exploratory Data Analysis (EDA)

Performed different types of exploratory analysis using Pandas, Matplotlib, Seaborn, and Plotly.

**Univariate Analysis**
- Individual variable distributions.
- Customer demographics.
- Order status distribution.
- Payment types and review scores.

**Bivariate Analysis**
- Revenue vs. product categories.
- Delivery time vs. review scores.
- Customer spending vs. purchase frequency.
- Seller performance comparisons.

**Multivariate Analysis**
- Relationships between multiple business variables.
- Customer behaviour and spending patterns.
- Delivery performance and customer satisfaction.

**Time Series Analysis**
- Monthly revenue trends.
- Order volume over time.
- Business performance patterns.

### 7️⃣ Statistical Analysis

Applied hypothesis testing to investigate business relationships and support analytical conclusions.

| Statistical Test | Business Question |
|---|---|
| Independent T-Test | Is there a significant difference in review scores between delayed and on-time deliveries? |
| ANOVA | Do average order values differ significantly across product categories? |
| Chi-Square Test | Is there an association between payment method and order status? |

Used statistical concepts such as:
- Null and Alternative Hypotheses.
- Significance Level (Alpha).
- P-Value.
- Statistical Decisions.
- Effect Size (Cohen's d).

### 8️⃣ Interactive Streamlit Dashboard

Developed an interactive dashboard using Streamlit, Plotly, Python, and MySQL.

The dashboard provides a business-focused overview of e-commerce performance through six major sections.

| Dashboard Section | Key Information |
|---|---|
| 📊 Business Overview | Revenue, orders, customers, sellers, AOV, and review scores |
| 💰 Sales Analysis | Revenue trends, monthly performance, and product category sales |
| 👥 Customer Analysis | Customer behaviour, spending, repeat purchases, and locations |
| 🏪 Seller & Product Analysis | Top sellers, seller revenue, and product categories |
| 🚚 Delivery Analysis | Delivery duration, delays, and on-time delivery performance |
| ⭐ Customer Experience | Review scores, customer satisfaction, and delivery-related reviews |

**Dashboard Features:**
- Interactive date filters.
- Dynamic KPI metrics.
- Business performance charts.
- Monthly revenue trends.
- Category and seller comparisons.
- Customer behaviour analysis.
- Delivery and review insights.
- MySQL database integration.

---

## 📁 Project Structure

```text
Cart2Insights/
│
├── data/
│   └── Raw CSV files
│
├── cleaned_data/
│   └── Cleaned CSV datasets
│
├── notebooks/
│   └── data_understanding_quality_cleaning.ipynb
│   └── sql_analysis.ipynb
│   └── feature_engineering.ipynb
│   └── eda.ipynb
│   └── statistical_analysis.ipynb
│
├── sql/
│   └── Cart2Insights.sql
│
├── ER Diagram.png
│
├── screenshots/
│   └── Dashboard screenshots
│
├── streamlit/
│   └── app.py
│   └── database.py
│   └── queries.py
│   └── requirements.txt
│   └── utils.py
│   
```

### Step 1: Clone the Repository

```bash
git clone [https://github.com/sowrinayagam08-lab/Cart2insights-olist-analytics.git]

cd cart2insights-olist-analytics
```

### Step 2: Install Required Libraries

```bash
pip install -r requirements.txt
```

### Step 3: Set Up MySQL Database

1. Open MySQL Workbench.
2. Start my MySQL connection.
3. Run the SQL scripts to create the database and tables.
4. Ensure the cleaned CSV datasets are available in the expected data folder.
5. Load the datasets into their respective tables.
6. Verify table records and relationships.

### Step 4: Configure Database Connection

Update my MySQL credentials in the notebook and dashboard application.

```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "*******"
DB_NAME = "cart2insights"
```

### Step 5: Run the Jupyter Notebook

Open `Cart2Insights.ipynb` and execute the cells in sequence to perform data preparation, database operations, feature engineering, EDA, and statistical analysis.

### Step 6: Launch the Streamlit Dashboard

Navigate to the folder containing `app.py` and execute:

```bash
streamlit run app.py
```

The dashboard will open in my browser.

---

## 💡 Key Learnings

Through this project, I gained practical experience in:

- Cleaning and preprocessing real-world datasets.
- Designing relational databases and understanding table relationships.
- Writing SQL queries from basic operations to advanced window functions.
- Connecting Python with MySQL.
- Performing feature engineering and exploratory data analysis.
- Applying statistical hypothesis testing to business problems.
- Developing interactive dashboards using Streamlit.
- Combining SQL, Python, and visualization tools into an end-to-end analytics workflow.

---

## 🚀 Future Improvements

- Develop customer segmentation using clustering algorithms.
- Build sales forecasting models.
- Create customer churn prediction models.
- Deploy the Streamlit dashboard online.
- Automate data refresh and reporting.

---

## 👩‍💻 About the Project Author

**Sowrinayagam**

AI & ML Learner

This project represents my hands-on learning journey in AI & ML, where I explored how raw data can be transformed into meaningful business insights using SQL, Python, statistics, and data visualization.

### Connect With Me

- 💼 LinkedIn: [Connect with me](https://www.linkedin.com/in/sowrinayagam-s-53224a2b5)
- 🐙 GitHub: [Explore my repositories](https://github.com/sowrinayagam08-lab/Cart2insights-olist-analytics.git)

---

<p align="center">
  <b>From Raw Data to Business Insights 🚀</b>
  <br>
  <i>Cart2Insights – Turning Data into Decisions.</i>
</p>
