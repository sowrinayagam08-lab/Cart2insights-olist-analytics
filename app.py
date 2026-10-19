"""
app.py  (v2)
------------
Main Streamlit entry point.  Run with:  streamlit run app.py
Sidebar: section navigation + Year and State filters (applied to every query).
"""

import streamlit as st

import queries as q
from database import run_query, test_connection
from utils import (bar_chart, empty_warning, fmt_int, fmt_money, insight_box,
                   kpi_row, line_chart, pie_chart, section_header, show,
                   state_map)

st.set_page_config(page_title="Cart2Insights | Olist Dashboard", page_icon="🛒", layout="wide")


# =====================================================================
# 1. BUSINESS OVERVIEW
# =====================================================================
def business_overview(p):
    section_header("Business Overview", "Headline KPIs for delivered orders")
    kpi = run_query(q.KPI_MAIN, p).iloc[0]
    if not kpi["total_orders"]:
        st.warning("No data for the selected filters. Try a different year or state.")
        return
    review = run_query(q.KPI_REVIEW, p).iloc[0]["avg_review_score"]

    kpi_row([
        ("Total Revenue", fmt_money(kpi["total_revenue"])),
        ("Total Orders", fmt_int(kpi["total_orders"])),
        ("Total Customers", fmt_int(kpi["total_customers"])),
    ])
    kpi_row([
        ("Total Sellers", fmt_int(kpi["total_sellers"])),
        ("Avg Order Value", fmt_money(kpi["avg_order_value"])),
        ("Avg Review Score", f"{review:.2f} / 5"),
    ])

    orders_per_customer = kpi["total_orders"] / kpi["total_customers"]
    insight_box(
        f"There are {orders_per_customer:.2f} orders per unique customer and an average order value of "
        f"{fmt_money(kpi['avg_order_value'])}.",
        "Orders per customer close to 1 means most buyers purchase only once.",
        "Growth depends on acquiring new customers; retention campaigns are an untapped lever.",
    )


# =====================================================================
# 2. SALES ANALYSIS
# =====================================================================
def sales_analysis(p):
    section_header("Sales Analysis", "Revenue trends, categories, products and locations")

    monthly = run_query(q.MONTHLY_REVENUE, p)
    if empty_warning(monthly):
        return
    show(line_chart(monthly, "month", "revenue", "Monthly Revenue Trend"))
    with st.expander("Month-over-month growth table"):
        st.dataframe(monthly, use_container_width=True)

    cat = run_query(q.REVENUE_BY_CATEGORY, p)
    state = run_query(q.SALES_BY_STATE, p)
    c1, c2 = st.columns(2)
    with c1:
        show(bar_chart(cat, "category", "revenue", "Top 15 Categories by Revenue", horizontal=True))
    with c2:
        show(bar_chart(state.head(10), "state", "revenue", "Top 10 States by Revenue"))

    if p["state"] == "All":
        show(state_map(state, "state", "revenue", "orders", "Sales by Location (bubble = revenue, colour = orders)"))

    st.subheader("Top-selling products")
    st.dataframe(run_query(q.TOP_PRODUCTS, p), use_container_width=True)

    top_cat = cat.iloc[0]
    top3_share = cat["revenue"].head(3).sum() / cat["revenue"].sum() * 100
    top_state = state.iloc[0]
    state_share = top_state["revenue"] / state["revenue"].sum() * 100
    peak = monthly.loc[monthly["revenue"].idxmax()]
    where = (f"{top_state['state']} contributes {state_share:.0f}% of revenue"
             if p["state"] == "All" else f"all figures are for {p['state']}")
    insight_box(
        f"'{top_cat['category']}' leads revenue, the top 3 categories make up {top3_share:.0f}% of the "
        f"top-15 total, {where}, and sales peaked in {peak['month']}.",
        "Revenue is concentrated in a few categories and regions, and sales are seasonal or campaign-driven.",
        "Prioritise stock and marketing for top categories, plan capacity for peak months, and reduce dependence on one region.",
    )


# =====================================================================
# 3. CUSTOMER ANALYSIS
# =====================================================================
def customer_analysis(p):
    section_header("Customer Analysis", "Who the customers are and how they spend")

    by_city = p["state"] != "All"
    dist = run_query(q.CUSTOMERS_BY_CITY if by_city else q.CUSTOMERS_BY_STATE, p)
    spend = run_query(q.CUSTOMER_SPENDING_BUCKETS, p)
    rvn = run_query(q.REPEAT_VS_NEW, p)
    if empty_warning(dist):
        return

    c1, c2 = st.columns(2)
    with c1:
        title = "Customer Distribution (Top 10 Cities)" if by_city else "Customer Distribution (Top 10 States)"
        show(bar_chart(dist.head(10), "location", "customers", title))
    with c2:
        show(pie_chart(rvn, "customer_type", "customers", "Repeat vs New Customers"))

    show(bar_chart(spend, "spend_bucket", "customers", "Customer Spending Distribution"))

    st.subheader("Top 10 customers by spend")
    st.dataframe(run_query(q.TOP_CUSTOMERS, p), use_container_width=True)

    repeat = rvn.loc[rvn["customer_type"].str.startswith("Repeat"), "customers"].sum()
    repeat_pct = repeat / rvn["customers"].sum() * 100
    insight_box(
        f"Only {repeat_pct:.1f}% of customers placed more than one order in this selection.",
        "The marketplace behaves like a one-time purchase platform with low loyalty.",
        "Even a small lift in repeat rate (loyalty offers, follow-up emails) would raise revenue without new acquisition cost.",
    )


# =====================================================================
# 4. SELLER & PRODUCT ANALYSIS
# =====================================================================
def seller_product_analysis(p):
    section_header("Seller & Product Analysis", "Seller performance and category economics")

    sellers = run_query(q.TOP_SELLERS, p)
    ratings = run_query(q.SELLER_RATINGS, p)
    cats = run_query(q.CATEGORY_PERFORMANCE, p)
    if empty_warning(sellers):
        return

    c1, c2 = st.columns(2)
    with c1:
        show(bar_chart(sellers.assign(seller=sellers["seller_id"].str[:8]),
                       "seller", "revenue", "Top 10 Sellers by Revenue"))
    with c2:
        if ratings.empty:
            st.info("Not enough orders per seller for ratings in this selection.")
        else:
            show(bar_chart(ratings.assign(seller=ratings["seller_id"].str[:8]),
                           "seller", "avg_review", "Top-Rated Sellers (10+ orders)"))

    st.subheader("Seller revenue and share")
    st.dataframe(sellers, use_container_width=True)

    st.subheader("Category performance (50+ units sold)")
    st.dataframe(cats, use_container_width=True)

    share = sellers["revenue_share_pct"].sum()
    insight_box(
        f"The top 10 sellers generate {share:.1f}% of revenue in this selection.",
        "A high share means revenue depends on a small group of sellers; a low share means it is spread widely.",
        "Protect and support top sellers (fulfilment, account management) and track seller ratings to catch quality drops early.",
    )


# =====================================================================
# 5. DELIVERY ANALYSIS
# =====================================================================
def delivery_analysis(p):
    section_header("Delivery Analysis", "Speed, punctuality and the effect on reviews")

    kpi = run_query(q.DELIVERY_KPI, p).iloc[0]
    if kpi["avg_delivery_days"] is None or kpi["avg_delivery_days"] != kpi["avg_delivery_days"]:
        st.warning("No data for the selected filters. Try a different year or state.")
        return
    kpi_row([
        ("Avg Delivery Time", f"{kpi['avg_delivery_days']} days"),
        ("On-time Deliveries", f"{kpi['on_time_pct']}%"),
    ])

    status = run_query(q.ON_TIME_VS_DELAYED, p)
    by_state = run_query(q.DELIVERY_BY_STATE, p)
    delay = run_query(q.DELAY_VS_REVIEW, p)

    c1, c2 = st.columns(2)
    with c1:
        show(pie_chart(status, "delivery_status", "orders", "On-time vs Delayed Orders"))
    with c2:
        if not by_state.empty:
            show(bar_chart(by_state, "state", "avg_delivery_days", "Avg Delivery Days by State"))

    if p["state"] == "All" and not by_state.empty:
        show(state_map(by_state, "state", "orders", "avg_delivery_days",
                       "Delivery Performance by Location (bubble = orders, colour = avg days)"))

    show(bar_chart(delay, "delay_bucket", "avg_review", "Delivery Delay vs Average Review Score"))

    on_time = delay.iloc[0]["avg_review"]
    worst = delay.iloc[-1]["avg_review"]
    if p["state"] == "All" and not by_state.empty:
        slowest = by_state.iloc[0]
        extra = f"{slowest['state']} has the slowest deliveries ({slowest['avg_delivery_days']} days)."
    else:
        extra = f"Average delivery time here is {kpi['avg_delivery_days']} days."
    insight_box(
        f"The best delay bucket averages {on_time} stars versus {worst} for the worst bucket. {extra}",
        "Delivery experience strongly influences customer satisfaction, and some regions are structurally slower.",
        "Improving logistics in slow regions and setting realistic delivery estimates would raise ratings and reduce complaints.",
    )


# =====================================================================
# 6. CUSTOMER EXPERIENCE
# =====================================================================
def customer_experience(p):
    section_header("Customer Experience", "Review scores and what drives them")

    dist = run_query(q.REVIEW_DISTRIBUTION, p)
    cats = run_query(q.REVIEWS_BY_CATEGORY, p)
    rating_time = run_query(q.RATING_BY_DELIVERY_TIME, p)
    if empty_warning(dist):
        return

    c1, c2 = st.columns(2)
    with c1:
        show(bar_chart(dist, "review_score", "reviews", "Review Score Distribution"))
    with c2:
        if not rating_time.empty:
            show(bar_chart(rating_time, "delivery_time", "avg_review", "Rating vs Delivery Time"))

    if cats.empty:
        st.info("Not enough reviews per category in this selection.")
        return
    show(bar_chart(cats, "category", "avg_review", "Lowest-Rated Categories (50+ reviews)", horizontal=True))

    low_pct = dist.loc[dist["review_score"] <= 2, "pct"].sum()
    worst_cat = cats.iloc[0]
    insight_box(
        f"{low_pct:.1f}% of reviews are 1-2 stars, and '{worst_cat['category']}' is the lowest-rated category ({worst_cat['avg_review']}).",
        "Dissatisfaction is a minority but is clustered in specific categories and long delivery times.",
        "Investigate quality and packaging in low-rated categories and speed up slow deliveries to lift overall ratings.",
    )


# =====================================================================
# NAVIGATION + FILTERS
# =====================================================================
SECTIONS = {
    "Business Overview": business_overview,
    "Sales Analysis": sales_analysis,
    "Customer Analysis": customer_analysis,
    "Seller & Product Analysis": seller_product_analysis,
    "Delivery Analysis": delivery_analysis,
    "Customer Experience": customer_experience,
}

st.sidebar.title("Cart2Insights")
st.sidebar.caption("Olist E-commerce Dashboard")
choice = st.sidebar.radio("Go to", list(SECTIONS))

if test_connection():
    st.sidebar.divider()
    st.sidebar.subheader("Filters")
    years = run_query(q.YEARS)["yr"].astype(int).tolist()
    states = run_query(q.STATES)["state"].tolist()
    year_label = st.sidebar.selectbox("Year", ["All"] + years)
    state_label = st.sidebar.selectbox("State", ["All"] + states)

    params = {"year": 0 if year_label == "All" else int(year_label), "state": state_label}
    st.caption(f"Showing: **{year_label}** | **{state_label}**")

    with st.spinner("Loading data..."):
        SECTIONS[choice](params)
