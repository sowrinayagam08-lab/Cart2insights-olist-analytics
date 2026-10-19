"""
queries.py  (v2 - filterable)
-----------------------------
All SQL lives here, grouped by dashboard section.

Every query accepts two parameters from the sidebar:
    :year   -> 0 means all years, otherwise e.g. 2017
    :state  -> 'All' or a state code such as 'SP'

Revenue = SUM(order_items.price) for delivered orders (freight excluded).
"""

# ---- Shared building blocks (constants, not user input, so safe to embed) ----
CJ = "JOIN customers c ON o.customer_id = c.customer_id"

F = """o.order_status = 'delivered'
      AND (:year = 0 OR YEAR(o.order_purchase_timestamp) = :year)
      AND (:state = 'All' OR c.customer_state = :state)"""

FD = F + " AND o.order_delivered_customer_date IS NOT NULL"


# =====================================================================
# FILTER OPTIONS (no parameters)
# =====================================================================
YEARS = """
SELECT DISTINCT YEAR(order_purchase_timestamp) AS yr
FROM orders
WHERE order_status = 'delivered'
ORDER BY yr;
"""

STATES = "SELECT DISTINCT customer_state AS state FROM customers ORDER BY state;"


# =====================================================================
# 1. BUSINESS OVERVIEW   (joins, aggregations, subquery)
# =====================================================================
KPI_MAIN = f"""
SELECT
    ROUND(SUM(oi.price), 2)                              AS total_revenue,
    COUNT(DISTINCT o.order_id)                           AS total_orders,
    COUNT(DISTINCT c.customer_unique_id)                 AS total_customers,
    COUNT(DISTINCT oi.seller_id)                         AS total_sellers,
    ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
{CJ}
WHERE {F};
"""

KPI_REVIEW = f"""
SELECT ROUND(AVG(r.review_score), 2) AS avg_review_score
FROM order_reviews r
WHERE r.order_id IN (
    SELECT o.order_id FROM orders o {CJ} WHERE {F}
);
"""  # subquery in WHERE


# =====================================================================
# 2. SALES ANALYSIS   (CTE + window LAG, GROUP BY, ORDER BY, LIMIT)
# =====================================================================
MONTHLY_REVENUE = f"""
WITH monthly AS (
    SELECT
        DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
        ROUND(SUM(oi.price), 2)                          AS revenue,
        COUNT(DISTINCT o.order_id)                       AS orders
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    {CJ}
    WHERE {F}
    GROUP BY month
)
SELECT
    month, revenue, orders,
    ROUND((revenue - LAG(revenue) OVER (ORDER BY month))
          / LAG(revenue) OVER (ORDER BY month) * 100, 1) AS mom_growth_pct
FROM monthly
ORDER BY month;
"""

REVENUE_BY_CATEGORY = f"""
SELECT
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
    ROUND(SUM(oi.price), 2) AS revenue,
    COUNT(*)                AS items_sold
FROM order_items oi
JOIN orders   o ON oi.order_id = o.order_id
{CJ}
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation t
       ON p.product_category_name = t.product_category_name
WHERE {F}
GROUP BY category
ORDER BY revenue DESC
LIMIT 15;
"""

TOP_PRODUCTS = f"""
SELECT
    oi.product_id,
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
    COUNT(*)                AS units_sold,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
JOIN orders   o ON oi.order_id = o.order_id
{CJ}
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation t
       ON p.product_category_name = t.product_category_name
WHERE {F}
GROUP BY oi.product_id, category
ORDER BY units_sold DESC
LIMIT 10;
"""

SALES_BY_STATE = f"""
SELECT
    c.customer_state           AS state,
    ROUND(SUM(oi.price), 2)    AS revenue,
    COUNT(DISTINCT o.order_id) AS orders
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
{CJ}
WHERE {F}
GROUP BY c.customer_state
ORDER BY revenue DESC;
"""


# =====================================================================
# 3. CUSTOMER ANALYSIS   (CTEs, CASE, window RANK)
# =====================================================================
CUSTOMERS_BY_STATE = f"""
SELECT c.customer_state AS location, COUNT(DISTINCT c.customer_unique_id) AS customers
FROM orders o
{CJ}
WHERE {F}
GROUP BY c.customer_state
ORDER BY customers DESC;
"""

CUSTOMERS_BY_CITY = f"""
SELECT c.customer_city AS location, COUNT(DISTINCT c.customer_unique_id) AS customers
FROM orders o
{CJ}
WHERE {F}
GROUP BY c.customer_city
ORDER BY customers DESC
LIMIT 10;
"""

CUSTOMER_SPENDING_BUCKETS = f"""
WITH customer_spend AS (
    SELECT c.customer_unique_id, SUM(oi.price) AS total_spent
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    {CJ}
    WHERE {F}
    GROUP BY c.customer_unique_id
)
SELECT
    CASE
        WHEN total_spent < 50   THEN '1. Under 50'
        WHEN total_spent < 100  THEN '2. 50 - 100'
        WHEN total_spent < 200  THEN '3. 100 - 200'
        WHEN total_spent < 500  THEN '4. 200 - 500'
        ELSE                         '5. 500+'
    END AS spend_bucket,
    COUNT(*) AS customers
FROM customer_spend
GROUP BY spend_bucket
ORDER BY spend_bucket;
"""

REPEAT_VS_NEW = f"""
WITH orders_per_customer AS (
    SELECT c.customer_unique_id, COUNT(DISTINCT o.order_id) AS n_orders
    FROM orders o
    {CJ}
    WHERE {F}
    GROUP BY c.customer_unique_id
)
SELECT
    CASE WHEN n_orders = 1 THEN 'New (1 order)' ELSE 'Repeat (2+ orders)' END AS customer_type,
    COUNT(*) AS customers
FROM orders_per_customer
GROUP BY customer_type;
"""

TOP_CUSTOMERS = f"""
WITH customer_spend AS (
    SELECT
        c.customer_unique_id,
        MAX(c.customer_state)      AS state,
        COUNT(DISTINCT o.order_id) AS orders,
        ROUND(SUM(oi.price), 2)    AS total_spent
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    {CJ}
    WHERE {F}
    GROUP BY c.customer_unique_id
)
SELECT RANK() OVER (ORDER BY total_spent DESC) AS spend_rank,
       customer_unique_id, state, orders, total_spent
FROM customer_spend
ORDER BY spend_rank
LIMIT 10;
"""


# =====================================================================
# 4. SELLER & PRODUCT ANALYSIS   (window SUM OVER, HAVING, derived table)
# =====================================================================
TOP_SELLERS = f"""
SELECT
    oi.seller_id,
    MAX(s.seller_state)        AS state,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.price), 2)    AS revenue,
    ROUND(SUM(oi.price) / SUM(SUM(oi.price)) OVER () * 100, 2) AS revenue_share_pct
FROM order_items oi
JOIN orders  o ON oi.order_id = o.order_id
{CJ}
JOIN sellers s ON oi.seller_id = s.seller_id
WHERE {F}
GROUP BY oi.seller_id
ORDER BY revenue DESC
LIMIT 10;
"""

SELLER_RATINGS = f"""
SELECT
    oi.seller_id,
    COUNT(DISTINCT o.order_id)    AS orders,
    ROUND(AVG(r.review_score), 2) AS avg_review
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
{CJ}
JOIN order_reviews r ON o.order_id = r.order_id
WHERE {F}
GROUP BY oi.seller_id
HAVING COUNT(DISTINCT o.order_id) >= 10
ORDER BY avg_review DESC, orders DESC
LIMIT 10;
"""

CATEGORY_PERFORMANCE = f"""
SELECT
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
    COUNT(*)                AS units_sold,
    ROUND(SUM(oi.price), 2) AS revenue,
    ROUND(AVG(oi.price), 2) AS avg_price,
    ROUND(AVG(rv.score), 2) AS avg_review
FROM order_items oi
JOIN orders   o ON oi.order_id = o.order_id
{CJ}
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation t
       ON p.product_category_name = t.product_category_name
LEFT JOIN (SELECT order_id, AVG(review_score) AS score
           FROM order_reviews GROUP BY order_id) rv
       ON o.order_id = rv.order_id
WHERE {F}
GROUP BY category
HAVING COUNT(*) >= 50
ORDER BY revenue DESC
LIMIT 15;
"""


# =====================================================================
# 5. DELIVERY ANALYSIS   (DATEDIFF, CASE, CTE)
# =====================================================================
DELIVERY_KPI = f"""
SELECT
    ROUND(AVG(DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp)), 1) AS avg_delivery_days,
    ROUND(AVG(o.order_delivered_customer_date <= o.order_estimated_delivery_date) * 100, 1) AS on_time_pct
FROM orders o
{CJ}
WHERE {FD};
"""

ON_TIME_VS_DELAYED = f"""
SELECT
    CASE WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date
         THEN 'On time' ELSE 'Delayed' END AS delivery_status,
    COUNT(*) AS orders
FROM orders o
{CJ}
WHERE {FD}
GROUP BY delivery_status;
"""

DELIVERY_BY_STATE = f"""
SELECT
    c.customer_state AS state,
    COUNT(*) AS orders,
    ROUND(AVG(DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp)), 1) AS avg_delivery_days,
    ROUND(AVG(o.order_delivered_customer_date > o.order_estimated_delivery_date) * 100, 1) AS delayed_pct
FROM orders o
{CJ}
WHERE {FD}
GROUP BY c.customer_state
HAVING COUNT(*) >= 20
ORDER BY avg_delivery_days DESC;
"""

DELAY_VS_REVIEW = f"""
WITH delivery AS (
    SELECT
        o.order_id,
        DATEDIFF(o.order_delivered_customer_date, o.order_estimated_delivery_date) AS days_late
    FROM orders o
    {CJ}
    WHERE {FD}
)
SELECT
    CASE
        WHEN d.days_late <= 0 THEN '1. On time / early'
        WHEN d.days_late <= 3 THEN '2. 1-3 days late'
        WHEN d.days_late <= 7 THEN '3. 4-7 days late'
        ELSE                       '4. 8+ days late'
    END AS delay_bucket,
    COUNT(*)                      AS orders,
    ROUND(AVG(r.review_score), 2) AS avg_review
FROM delivery d
JOIN order_reviews r ON d.order_id = r.order_id
GROUP BY delay_bucket
ORDER BY delay_bucket;
"""


# =====================================================================
# 6. CUSTOMER EXPERIENCE
# =====================================================================
REVIEW_DISTRIBUTION = f"""
SELECT r.review_score, COUNT(*) AS reviews,
       ROUND(COUNT(*) * 100 / SUM(COUNT(*)) OVER (), 1) AS pct
FROM order_reviews r
JOIN orders o ON r.order_id = o.order_id
{CJ}
WHERE {F}
GROUP BY r.review_score
ORDER BY r.review_score;
"""

REVIEWS_BY_CATEGORY = f"""
SELECT
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
    COUNT(DISTINCT r.review_id)   AS reviews,
    ROUND(AVG(r.review_score), 2) AS avg_review
FROM order_reviews r
JOIN orders o       ON r.order_id = o.order_id
{CJ}
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p     ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation t
       ON p.product_category_name = t.product_category_name
WHERE {F}
GROUP BY category
HAVING COUNT(DISTINCT r.review_id) >= 50
ORDER BY avg_review ASC
LIMIT 15;
"""

RATING_BY_DELIVERY_TIME = f"""
SELECT
    CASE
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp) <= 7  THEN '1. 0-7 days'
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp) <= 14 THEN '2. 8-14 days'
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp) <= 21 THEN '3. 15-21 days'
        ELSE '4. 22+ days'
    END AS delivery_time,
    COUNT(*) AS orders,
    ROUND(AVG(r.review_score), 2) AS avg_review
FROM orders o
{CJ}
JOIN order_reviews r ON o.order_id = r.order_id
WHERE {FD}
GROUP BY delivery_time
ORDER BY delivery_time;
"""
