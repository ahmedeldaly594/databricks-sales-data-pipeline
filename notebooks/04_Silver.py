df = spark.table("sales_project.bronze.bronze_sales")
from pyspark.sql.functions import *

# COMMAND ----------

%md
Changing data types

# COMMAND ----------

df = df.withColumn("quantity",col("quantity").cast("int"))
df = df.withColumn("transaction_date",col("transaction_date").cast("date"))
df = df.withColumn("discount_applied",col("discount_applied").cast("boolean"))

# COMMAND ----------

%md
nulls handling

# COMMAND ----------

%md
Drop nulls

# COMMAND ----------

df = df.dropna(subset=["quantity","total_spent","price_per_unit"])

# COMMAND ----------

%md
fill nulls

# COMMAND ----------

df = df.fillna({"item": "Unknown"})

# COMMAND ----------

df.createOrReplaceTempView("Silver_source")

# COMMAND ----------

%sql
CREATE TABLE IF NOT EXISTS sales_project.silver.silver_sales
                AS 
                SELECT * FROM silver_source

# COMMAND ----------

%md
Merge

# COMMAND ----------

%sql
MERGE INTO sales_project.silver.silver_sales
USING silver_source
ON sales_project.silver.silver_sales.transaction_id = silver_source.transaction_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
