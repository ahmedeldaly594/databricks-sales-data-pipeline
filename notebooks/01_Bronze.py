from datetime import timedelta
from pyspark.sql.functions import *

if spark.catalog.tableExists("sales_project.bronze.bronze_sales"):
    last_transaction_date = spark.sql(
        "SELECT MAX(transaction_date) FROM sales_project.bronze.bronze_sales"
    ).collect()[0][0]
else:
    last_transaction_date = "1000-01-01"

incremental_start_date = (
    last_transaction_date - timedelta(days=1)
    if last_transaction_date != "1000-01-01"
    else last_transaction_date
)

# COMMAND ----------

last_transaction_date

# COMMAND ----------

spark.sql(f"""
select * from sales_project.default.sales_raw
WHERE Transaction_Date >= '{incremental_start_date}'
""").createOrReplaceTempView('bronze_source')

# COMMAND ----------

%sql
select * from bronze_source limit 10

# COMMAND ----------

%sql
 create or replace table sales_project.bronze.bronze_sales
 as
 select * from bronze_source
