df = spark.table("sales_project.bronze.bronze_sales")
from pyspark.sql.functions import *

# COMMAND ----------

%md
Rule 1 — transaction_id must not be null

# COMMAND ----------

null_transaction_id = df.filter(
    col("transaction_id").isNull()
).count()

status = "PASS" if null_transaction_id == 0 else "FAIL"

print(f"Rule: transaction_id must not be null")
print(f"Invalid records: {null_transaction_id}")
print(f"Status: {status}")

# COMMAND ----------

%md
Rule 2 — customer_id must not be null

# COMMAND ----------

null_customer_id = df.filter(
    col("customer_id").isNull()
).count()

status = "PASS" if null_customer_id == 0 else "FAIL"

print("Rule: customer_id must not be null")
print(f"Invalid records: {null_customer_id}")
print(f"Status: {status}")

# COMMAND ----------

invalid_total_calculation = df.filter(
    col("price_per_unit").isNotNull() &
    col("quantity").isNotNull() &
    col("total_spent").isNotNull() &
    (col("total_spent") != col("price_per_unit") * col("quantity"))
).count()

status = "PASS" if invalid_total_calculation == 0 else "FAIL"

print("Rule: total_spent must equal price_per_unit * quantity")
print(f"Invalid records: {invalid_total_calculation}")
print(f"Status: {status}")

# COMMAND ----------

%md
Rule 3 - Transaction id must be unique

# COMMAND ----------

duplicate_transaction_id = df.groupBy("transaction_id") \
    .count() \
    .filter(col("count") > 1) \
    .count()

status = "PASS" if duplicate_transaction_id == 0 else "FAIL"

print("Rule: transaction_id must be unique")
print(f"Duplicate transaction IDs: {duplicate_transaction_id}")
print(f"Status: {status}")

# COMMAND ----------

%md
Data quality summary

# COMMAND ----------

quality_results = [
    ("transaction_id not null", null_transaction_id),
    ("customer_id not null", null_customer_id),
    ("transaction_id unique", duplicate_transaction_id),
    ("total_spent = price_per_unit * quantity", invalid_total_calculation)
]

quality_df = spark.createDataFrame(
    quality_results,
    ["rule", "invalid_records"]
)

quality_df = quality_df.withColumn(
    "status",
    when(col("invalid_records") == 0, "PASS")
    .otherwise("FAIL")
)

display(quality_df)
