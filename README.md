Cart2Insights: Olist E-commerce Analytics

An end-to-end data analytics project on the Olist Brazilian e-commerce dataset. The project cleans the raw data, stores it in a MySQL database, analyses it with SQL and Python, and shows the results in an interactive Streamlit dashboard.

Project Goal

To turn raw e-commerce data into clear business insights. The project answers questions about sales, customers, sellers, products, delivery, and customer experience.

Tools Used
Area	Tools
Language	Python, SQL
Database	MySQL (MySQL Workbench)
Data work	Pandas, NumPy
Visuals	Matplotlib, Seaborn, Plotly
Statistics	SciPy (t-test, ANOVA, chi-square)
Dashboard	Streamlit
Notebooks	Jupyter Notebook
Editor	VS Code
Dataset

The Olist dataset has 9 tables:

customers
geolocation
order_items
order_payments
order_reviews
orders
products
sellers
product_category_name_translation

All 9 tables were cleaned before loading into the database.

Project Steps
Data cleaning: cleaned all 9 CSV files.
Database design: created the database and tables using the ER diagram.
Data loading: loaded the cleaned CSV files into MySQL using LOAD DATA LOCAL INFILE.
Constraints: added primary keys and foreign keys.
Verification: checked row counts and relationships after loading.
SQL analysis: answered business questions using:
SELECT, WHERE, ORDER BY
GROUP BY, HAVING
Joins
Subqueries
CTEs
Window functions
Python connection: connected MySQL to Jupyter Notebook.
Feature engineering: created new useful columns from the existing data.
EDA: explored patterns and trends with charts.
Statistical analysis: used t-test, ANOVA, and chi-square tests.
Dashboard: built an interactive Streamlit app connected to the database.
Dashboard Sections

The Streamlit dashboard has six sections:

Section	What it shows
Business Overview	Main KPIs of the business
Sales	Sales and revenue trends
Customer	Customer behaviour and location
Seller & Product	Top sellers and product categories
Delivery	Delivery time and delays
Customer Experience	Reviews and ratings
Project Structure
Cart2Insights/
│
├── data/                # Cleaned CSV files
├── notebooks/           # Cleaning, feature engineering, EDA, statistics
├── sql/                 # Database, table, and analysis queries
├── dashboard/           # Streamlit app
├── images/              # Screenshots and ER diagram
├── requirements.txt
└── README.md

Change the folder names above to match your real project folders.

How to Run

1. Clone the repository

bash
git clone https://github.com/<your-username>/cart2insights-olist-analytics.git
cd cart2insights-olist-analytics

2. Install the libraries

bash
pip install -r requirements.txt

3. Set up the database

Open MySQL Workbench.
Run the SQL files to create the database and tables.
Load the cleaned CSV files from the data folder.

4. Update the database details

In the dashboard code, change the MySQL host, user, password, and database name to your own.

5. Run the dashboard

bash
streamlit run dashboard/app.py

Key Learnings
Designing a relational database with primary and foreign keys
Writing SQL from basic queries to CTEs and window functions
Connecting SQL, Python, and Streamlit in one workflow
Using statistical tests to support business conclusions

Author
<Sowrinayagam> LinkedIn | GitHub
