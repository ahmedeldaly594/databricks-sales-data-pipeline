df = spark.table("sales_project.silver.silver_sales")
df.display()

# COMMAND ----------

%md
Dim customer

# COMMAND ----------

%sql
CREATE OR REPLACE TABLE sales_project.gold.dim_customer
AS 
with rem_dub AS (

SELECT DISTINCT customer_id 
from sales_project.silver.silver_sales

)

SELECT customer_id , row_number() over (order by customer_id) as customer_key
from rem_dub

# COMMAND ----------

%sql
select * from sales_project.gold.dim_customer

# COMMAND ----------

%md
Dim Item

# COMMAND ----------

%sql
CREATE OR REPLACE TABLE sales_project.gold.dim_item
AS WITH rem_dub AS (
SELECT DISTINCT item , category
FROM sales_project.silver.silver_sales

)
SELECT item , category , row_number() over (order by item) as item_key
FROM rem_dub

# COMMAND ----------

%md
Dim location

# COMMAND ----------

%sql
CREATE OR REPLACE TABLE sales_project.gold.dim_location
AS WITH rem_dub AS (
SELECT DISTINCT Location
FROM sales_project.silver.silver_sales

)
SELECT location, row_number() over (order by location) as location_key
FROM rem_dub

# COMMAND ----------

%md
Dim payment

# COMMAND ----------

%sql
CREATE OR REPLACE TABLE sales_project.gold.dim_payment
AS WITH rem_dub AS (
SELECT DISTINCT payment_method
FROM sales_project.silver.silver_sales

)
SELECT payment_method, row_number() over (order by payment_method) as payment_key
FROM rem_dub

# COMMAND ----------

%md
Dim Discount

# COMMAND ----------

%sql
CREATE OR REPLACE TABLE sales_project.gold.dim_discount
AS WITH rem_dub AS (
SELECT DISTINCT discount_applied
FROM sales_project.silver.silver_sales

)
SELECT discount_applied, row_number() over (order by discount_applied) as discount_key
FROM rem_dub

# COMMAND ----------

%md
Dim sales

# COMMAND ----------

%sql
CREATE OR REPLACE TABLE sales_project.gold.dim_sales

SELECT row_number() over (order by transaction_id) as sales_key , transaction_id , customer_id , payment_method ,
 discount_applied , item , category ,
  transaction_date , location 

FROM sales_project.silver.silver_sales

# COMMAND ----------

%md
Fact Sales

# COMMAND ----------

%sql

CREATE OR REPLACE TABLE sales_project.gold.fact_sales AS

SELECT
    s.sales_key,
    c.customer_key,
    i.item_key,
    l.location_key,
    p.payment_key,
    d.discount_key,
    f.quantity,
    f.price_per_unit,
    f.total_spent

FROM sales_project.silver.silver_sales f

LEFT JOIN sales_project.gold.dim_customer c
    ON c.customer_id = f.customer_id

LEFT JOIN sales_project.gold.dim_item i
    ON i.item = f.item
    AND i.category = f.category

LEFT JOIN sales_project.gold.dim_location l
    ON l.location = f.location

LEFT JOIN sales_project.gold.dim_payment p
    ON p.payment_method = f.payment_method

LEFT JOIN sales_project.gold.dim_discount d
    ON d.discount_applied <=> f.discount_applied

LEFT JOIN sales_project.gold.dim_sales s
    ON s.transaction_id = f.transaction_id

# COMMAND ----------

%sql
select * from sales_project.gold.fact_sales order by sales_key
