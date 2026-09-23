%md
Read Data

# COMMAND ----------

df = spark.table("sales_project.bronze.bronze_sales")

# COMMAND ----------

%md
Null profiling

# COMMAND ----------

from pyspark.sql.functions import *

null_profile = df.select([
    sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in df.columns
])

display(null_profile)

# COMMAND ----------

%md
dublicates profiling

# COMMAND ----------

total_rows = df.count()
distinct_rows = df.distinct().count()

print("Total Rows:", total_rows)
print("Distinct Rows:", distinct_rows)
print("Duplicate Rows:", total_rows - distinct_rows)

# COMMAND ----------

%md
Check if transaction_id is unique

# COMMAND ----------

df.select(
    countDistinct("transaction_id").alias("distinct_transaction_ids")
).show()

# COMMAND ----------

%md
Checking data format

# COMMAND ----------

df.select("transaction_date").distinct().display()

# COMMAND ----------

%md
find max & min Date

# COMMAND ----------

df.select(
    min("transaction_date").alias("min_transaction_date"),
    max("transaction_date").alias("max_transaction_date")
).show()

# COMMAND ----------

%md
checking invalid values

# COMMAND ----------

display(
    df.groupBy("payment_method")
    .count()
    .orderBy("count", ascending=False)
)

# COMMAND ----------

display(
    df.groupBy("category")
    .count()
    .orderBy("count", ascending=False)
)

# COMMAND ----------

display(
    df
    .groupBy("discount_applied")
    .count()
    .orderBy("count", ascending=False)
)
