# Step 1: Create the database

DROP DATABASE IF EXISTS olist_db;
CREATE DATABASE olist_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE olist_db;

# Step 2: Create tables

CREATE TABLE customers (
    ID INT,
    customer_id CHAR(32) NOT NULL,
    customer_unique_id CHAR(32),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state CHAR(2)
);

CREATE TABLE geolocation (
    geolocation_zip_code_prefix INT NOT NULL,
    lat DOUBLE,
    lng DOUBLE,
    city VARCHAR(100),
    state CHAR(2)
);

CREATE TABLE sellers (
    ID INT,
    seller_id CHAR(32) NOT NULL,
    seller_zip_code_prefix INT,
    seller_city VARCHAR(100),
    seller_state CHAR(2)
);

CREATE TABLE product_category_name_translation (
    ID INT,
    product_category_name VARCHAR(100) NOT NULL,
    product_category_name_english VARCHAR(100),
    category_label VARCHAR(100)
);

CREATE TABLE products (
    ID INT,
    product_id CHAR(32) NOT NULL,
    product_category_name VARCHAR(100),
    product_name_length INT NULL,
    product_description_length INT NULL,
    product_photos_qty INT NULL,
    product_weight_g DECIMAL(10,1) NULL,
    product_length_cm DECIMAL(10,1) NULL,
    product_height_cm DECIMAL(10,1) NULL,
    product_width_cm DECIMAL(10,1) NULL,
    product_volume_cm3 DECIMAL(12,1) NULL
);

CREATE TABLE orders (
    ID INT,
    order_id CHAR(32) NOT NULL,
    customer_id CHAR(32) NOT NULL,
    order_status VARCHAR(20),
    order_purchase_timestamp DATETIME,
    order_approved_at DATETIME NULL,
    order_delivered_carrier_date DATETIME NULL,
    order_delivered_customer_date DATETIME NULL,
    order_estimated_delivery_date DATE,
    date_issue BOOLEAN,
    delivery_days DECIMAL(6,1) NULL,
    estimated_days INT,
    delay_days DECIMAL(6,1) NULL,
    is_late BOOLEAN,
    purchase_month CHAR(7)
);

CREATE TABLE order_items (
    ID INT,
    order_id CHAR(32) NOT NULL,
    order_item_id INT NOT NULL,
    product_id CHAR(32) NOT NULL,
    seller_id CHAR(32) NOT NULL,
    shipping_limit_date DATETIME,
    price DECIMAL(10,2),
    freight_value DECIMAL(10,2),
    total_value DECIMAL(10,2)
);

CREATE TABLE order_payments (
    ID INT,
    order_id CHAR(32) NOT NULL,
    payment_sequential INT NOT NULL,
    payment_type VARCHAR(20),
    payment_installments INT,
    payment_value DECIMAL(10,2)
);	

CREATE TABLE order_reviews (
    ID INT,
    review_id CHAR(32) NOT NULL,
    order_id CHAR(32) NOT NULL,
    review_score TINYINT,
    review_comment_title VARCHAR(255) NULL,
    review_comment_message TEXT NULL,
    review_creation_date DATETIME,
    review_answer_timestamp DATETIME
);


# Step 3: Load the cleaned CSVs

SET GLOBAL local_infile = 1;

LOAD DATA LOCAL INFILE 'C:/Cleaned data/olist_customers_cleaned.csv'
INTO TABLE customers
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE 'C:/Cleaned data/olist_geolocation_cleaned.csv'
INTO TABLE geolocation
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;	

LOAD DATA LOCAL INFILE 'C:/Cleaned data/olist_sellers_cleaned.csv'
INTO TABLE sellers
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE 'C:/Cleaned data/product_category_name_translation_cleaned.csv'
INTO TABLE product_category_name_translation
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE 'C:/Cleaned data/olist_order_items_cleaned.csv'
INTO TABLE order_items
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

SELECT count(*)
FROM order_items;

LOAD DATA LOCAL INFILE 'C:/Cleaned data/olist_order_payments_cleaned.csv'
INTO TABLE order_payments
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

# These three tables have empty cells or True/False text, so they use variables to convert them:

LOAD DATA LOCAL INFILE 'C:/Cleaned data/olist_products_cleaned.csv'
INTO TABLE products
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(ID, product_id, product_category_name, @name_len, @desc_len, @photos,
 @weight, @len, @height, @width, @volume)
SET product_name_length        = NULLIF(@name_len, ''),
    product_description_length = NULLIF(@desc_len, ''),
    product_photos_qty         = NULLIF(@photos, ''),
    product_weight_g           = NULLIF(@weight, ''),
    product_length_cm          = NULLIF(@len, ''),
    product_height_cm          = NULLIF(@height, ''),
    product_width_cm           = NULLIF(@width, ''),
    product_volume_cm3         = NULLIF(@volume, '');
    
LOAD DATA LOCAL INFILE 'C:/Cleaned data/olist_orders_cleaned.csv'
INTO TABLE orders
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(ID, order_id, customer_id, order_status, order_purchase_timestamp,
 @approved, @carrier, @delivered, order_estimated_delivery_date,
 @date_issue, @delivery_days, estimated_days, @delay_days, @is_late, purchase_month)
SET order_approved_at             = NULLIF(@approved, ''),
    order_delivered_carrier_date  = NULLIF(@carrier, ''),
    order_delivered_customer_date = NULLIF(@delivered, ''),
    date_issue    = (@date_issue = 'True'),
    delivery_days = NULLIF(@delivery_days, ''),
    delay_days    = NULLIF(@delay_days, ''),
    is_late       = (@is_late = 'True');
    
    
LOAD DATA LOCAL INFILE 'C:/Cleaned data/olist_order_reviews_cleaned.csv'
INTO TABLE order_reviews
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(ID, review_id, order_id, review_score, @title, @message,
 review_creation_date, review_answer_timestamp)
SET review_comment_title   = NULLIF(@title, ''),
    review_comment_message = NULLIF(@message, '');
    
    
# Step 4: Add primary and foreign keys

# Primary keys
ALTER TABLE customers  ADD PRIMARY KEY (customer_id);
ALTER TABLE sellers    ADD PRIMARY KEY (seller_id);
ALTER TABLE products   ADD PRIMARY KEY (product_id);
ALTER TABLE orders     ADD PRIMARY KEY (order_id);
ALTER TABLE geolocation ADD PRIMARY KEY (geolocation_zip_code_prefix);
ALTER TABLE product_category_name_translation ADD PRIMARY KEY (product_category_name);
ALTER TABLE order_items    ADD PRIMARY KEY (order_id, order_item_id);
ALTER TABLE order_payments ADD PRIMARY KEY (order_id, payment_sequential);
ALTER TABLE order_reviews  ADD PRIMARY KEY (review_id, order_id);

# Foreign keys. All of these pass on your data (0 orphan rows).

ALTER TABLE orders
  ADD CONSTRAINT fk_orders_customer
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

ALTER TABLE order_items
  ADD CONSTRAINT fk_items_order
  FOREIGN KEY (order_id) REFERENCES orders(order_id);

ALTER TABLE order_items
  ADD CONSTRAINT fk_items_product
  FOREIGN KEY (product_id) REFERENCES products(product_id);

ALTER TABLE order_items
  ADD CONSTRAINT fk_items_seller
  FOREIGN KEY (seller_id) REFERENCES sellers(seller_id);

ALTER TABLE order_payments
  ADD CONSTRAINT fk_payments_order
  FOREIGN KEY (order_id) REFERENCES orders(order_id);

ALTER TABLE order_reviews
  ADD CONSTRAINT fk_reviews_order
  FOREIGN KEY (order_id) REFERENCES orders(order_id);
  
# Step 5: Verify the data

SELECT 'customers' AS tbl, COUNT(*) AS n FROM customers
UNION ALL SELECT 'geolocation', COUNT(*) FROM geolocation
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL SELECT 'order_payments', COUNT(*) FROM order_payments
UNION ALL SELECT 'order_reviews', COUNT(*) FROM order_reviews
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'sellers', COUNT(*) FROM sellers
UNION ALL SELECT 'category_translation', COUNT(*) FROM product_category_name_translation;

# 5.2 Constraints exist
SELECT TABLE_NAME, CONSTRAINT_NAME, CONSTRAINT_TYPE
FROM information_schema.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'olist_db'
ORDER BY TABLE_NAME, CONSTRAINT_TYPE;

# 5.3 NULL checks. Expected: 160 / 1783 / 2965 in orders; 610 and 2 in products.
SELECT
  SUM(order_approved_at IS NULL)             AS null_approved,
  SUM(order_delivered_carrier_date IS NULL)  AS null_carrier,
  SUM(order_delivered_customer_date IS NULL) AS null_delivered,
  SUM(delivery_days IS NULL)                 AS null_delivery_days
FROM orders;

SELECT
  SUM(product_name_length IS NULL) AS null_name_len,
  SUM(product_weight_g IS NULL)    AS null_weight
FROM products;

# 5.4 Booleans loaded correctly
SELECT is_late, date_issue, COUNT(*) AS n
FROM orders
GROUP BY is_late, date_issue;

# 5.5 Orphan checks. Every result should be 0.
SELECT COUNT(*) FROM orders o LEFT JOIN customers c ON o.customer_id = c.customer_id WHERE c.customer_id IS NULL;
SELECT COUNT(*) FROM order_items i LEFT JOIN orders o ON i.order_id = o.order_id WHERE o.order_id IS NULL;
SELECT COUNT(*) FROM order_items i LEFT JOIN products p ON i.product_id = p.product_id WHERE p.product_id IS NULL;
SELECT COUNT(*) FROM order_items i LEFT JOIN sellers s ON i.seller_id = s.seller_id WHERE s.seller_id IS NULL;
SELECT COUNT(*) FROM order_payments p LEFT JOIN orders o ON p.order_id = o.order_id WHERE o.order_id IS NULL;
SELECT COUNT(*) FROM order_reviews r LEFT JOIN orders o ON r.order_id = o.order_id WHERE o.order_id IS NULL;

# 5.6 Value and date sanity
SELECT MIN(order_purchase_timestamp), MAX(order_purchase_timestamp) FROM orders;
SELECT order_status, COUNT(*) FROM orders GROUP BY order_status;
SELECT payment_type, COUNT(*) FROM order_payments GROUP BY payment_type;
SELECT review_score, COUNT(*) FROM order_reviews GROUP BY review_score ORDER BY review_score;
SELECT MIN(price), MAX(price), MIN(freight_value), MAX(freight_value) FROM order_items;


# 5.3 Join test
SELECT c.customer_state, COUNT(DISTINCT o.order_id) AS orders, ROUND(SUM(i.price),2) AS revenue
FROM customers c
JOIN orders o      ON c.customer_id = o.customer_id
JOIN order_items i ON o.order_id = i.order_id
GROUP BY c.customer_state
ORDER BY revenue DESC
LIMIT 5;

# Step 9: T-Test on Delivery Delay vs Review Score

/*
Step 1: Define the hypotheses
Group 1 (On Time): delivered on or before the estimated delivery date
Group 2 (Delayed): delivered after the estimated delivery date
H₀: mean review score (Delayed) = mean review score (On Time)
H₁: mean review score (Delayed) < mean review score (On Time) (one-tailed, because your question asks about lower scores)
Significance level: α = 0.05

Step 2: Define “delayed” and filter the data
Use only orders with order_status = 'delivered'.
Both order_delivered_customer_date and order_estimated_delivery_date must be non-null.
Delayed means order_delivered_customer_date > order_estimated_delivery_date.
Some orders have more than one review. Average the score per order so each order counts once. 
Otherwise the observations are not independent, which breaks a t-test assumption.
*/

# Step 3: Extract the data in SQL (MySQL)
SELECT
    delivery_status,
    COUNT(*)                       AS n_orders,
    ROUND(AVG(review_score), 3)    AS avg_score,
    ROUND(STDDEV(review_score), 3) AS std_score
FROM (
    SELECT
        o.order_id,
        r.review_score,
        CASE
            WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
                THEN 'Delayed'
            ELSE 'On Time'
        END AS delivery_status,
        DATEDIFF(o.order_delivered_customer_date,
                 o.order_estimated_delivery_date) AS delay_days
    FROM orders o
    JOIN (
        SELECT order_id, AVG(review_score) AS review_score
        FROM order_reviews
        GROUP BY order_id
    ) r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
      AND o.order_estimated_delivery_date IS NOT NULL
) t
GROUP BY delivery_status;