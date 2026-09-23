Databricks Sales Data Pipeline

An end-to-end sales data pipeline built with Databricks, PySpark, Spark SQL, and Delta Lake.

The project demonstrates how sales data can be ingested, profiled, quality-checked, cleaned, transformed, and modeled into analytical tables using a Medallion Architecture.

Architecture




Pipeline Flow
Source Table

    ↓

Bronze

    ↓

Silver

    ↓

Gold
Technologies
Databricks
PySpark
Spark SQL
Delta Lake
SQL
Python
Medallion Architecture
Incremental Data Loading
Data Quality Checks
Data Modeling
Project Structure
databricks-sales-data-pipeline/

│
├── notebooks/
│   ├── 01_Bronze.py
│   ├── 02_Data_Profiling.py
│   ├── 03_Data_Quality.py
│   ├── 04_Silver.py
│   └── 05_Gold.py
│
├── data/
│   └── README.md
│
├── docs/
│   └── architecture.png
│
├── .gitignore
└── README.md
Bronze Layer

The Bronze layer reads the source sales table and applies a date-based incremental extraction strategy.

The pipeline uses the maximum transaction date already present in Bronze as a watermark. A one-day overlap is used when calculating the next extraction window to reduce the risk of missing records around the watermark boundary.

Data Profiling

The profiling notebook checks characteristics of the Bronze data, including:

Null values
Duplicate rows
Transaction ID uniqueness
Date range
Category distribution
Payment method distribution
Discount distribution

The profiling notebook is used for data inspection and analysis and is not configured as a task in the Databricks workflow.

Data Quality

The Data Quality notebook contains explicit rules for:

transaction_id not null
customer_id not null
transaction_id uniqueness
total_spent = price_per_unit × quantity

The notebook produces PASS/FAIL-style results and an overall quality summary.

Note: Data Quality is currently implemented as a supporting validation notebook and is not configured as a blocking task in the Databricks workflow.

Silver Layer

The Silver layer applies data cleaning and transformation, including:

Data type casting
Null handling
Removing records with missing critical numeric fields
Replacing missing item values with Unknown
MERGE-based upsert using transaction_id

The resulting table is:

sales_project.silver.silver_sales
Gold Layer

The Gold layer creates analytical tables from the Silver data.

Current tables include:

sales_project.gold.dim_customer

sales_project.gold.dim_item

sales_project.gold.dim_location

sales_project.gold.dim_payment

sales_project.gold.dim_discount

sales_project.gold.dim_sales

sales_project.gold.fact_sales

The model uses dimension tables and a fact table to support analytical queries.

Incremental Loading

The incremental strategy is based on transaction_date:

Read the current maximum transaction date from Bronze.
Subtract one day to create an overlap window.
Read source records from that date onward.
Process the incoming records through Silver.
Use MERGE in Silver based on transaction_id.

This approach demonstrates an incremental ETL pattern using a date-based watermark and overlap window.

Databricks Workflow

The Databricks workflow runs the main transformation notebooks in dependency order:

01_Bronze

    ↓

04_Silver

    ↓

05_Gold

Profiling and Data Quality remain available as supporting notebooks for data inspection and quality analysis and are not part of the main workflow execution.

Future Improvements
Add a blocking Data Quality Gate to the Databricks workflow.
Use stable surrogate-key management for Gold dimensions.
Add automated tests for schema and business rules.
Add cloud storage as an external source.
Add orchestration and monitoring improvements.