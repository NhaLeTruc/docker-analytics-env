from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import DateType, StringType, IntegerType, LongType, DoubleType, TimestampType
from pyspark.sql.window import Window
import argparse

def main(dim_customer_path, dim_store_path, dim_product_path, fact_sales_path):
    # Create Spark session
    spark = (SparkSession.builder
        .appName("BronzeToSilver")
        .config("hive.metastore.uris", "thrift://hive-metastore:9083")
        .enableHiveSupport()
        .getOrCreate())

    print("Bronze to Silver: Spark session created.")

    try:
        # Read from bronze table (data has already been de-duped and nulls removed)
        bronze_df = spark.table("retail_sales_db.raw_data")
        print("Successfully read from table retail_sales_db.raw_data")

        # --- Silver Layer Data Quality Checks (Business Rules & Consistency) ---
        
        # Data arrives with correct types from Bronze layer, so we can proceed with business logic.
        silver_df = bronze_df

        # 1. Consistency: Trim whitespace from all string columns
        string_cols = [c.name for c in silver_df.schema.fields if isinstance(c.dataType, StringType)]
        for col_name in string_cols:
            silver_df = silver_df.withColumn(col_name, f.trim(f.col(col_name)))

        # 2. Accepted Values & Consistency: Clean phone number format
        # Product category and numeric validity are now handled in Bronze
        silver_df = silver_df.fillna({"product_name": "Unknown"})
        silver_df = silver_df.withColumn("customer_phone", f.concat(f.lit('+'), f.regexp_replace(f.col("customer_phone"), "[^0-9]", "")))

        silver_df.cache()
        print("Applied Silver DQ checks and business transformations.")
        
        # --- Create Dimension and Fact Tables (with unique dimension keys) ---
        
        dim_customer = silver_df.withColumn("row_num", f.row_number().over(Window.partitionBy("customer_id").orderBy(f.col("transaction_timestamp").desc()))) \
                                .filter(f.col("row_num") == 1) \
                                .select('customer_id', 'customer_name', 'customer_gender', 'customer_dob', 'customer_email', 'customer_phone', 'customer_city', 'customer_state')
        
        dim_store = silver_df.withColumn("row_num", f.row_number().over(Window.partitionBy("store_id").orderBy(f.col("transaction_timestamp").desc()))) \
                             .filter(f.col("row_num") == 1) \
                             .select('store_id', 'store_name', 'store_city', 'store_state')

        dim_product = silver_df.withColumn("row_num", f.row_number().over(Window.partitionBy("product_id").orderBy(f.col("transaction_timestamp").desc()))) \
                               .filter(f.col("row_num") == 1) \
                               .select('product_id', 'product_name', 'product_category')

        fact_sales = silver_df.select('transaction_id', 'transaction_timestamp', 'quantity', 'unit_price', 'total_amount', 'payment_method', 'customer_id', 'store_id', 'product_id')

        # Write dimension and fact tables to Silver layer
        print("Writing dimension and fact tables to Silver layer")

        spark.sql("DROP TABLE IF EXISTS retail_sales_db.dim_customer")
        (dim_customer.write.format("delta").mode("overwrite").option("path", dim_customer_path).option("overwriteSchema", "true").saveAsTable("retail_sales_db.dim_customer"))
        
        spark.sql("DROP TABLE IF EXISTS retail_sales_db.dim_store")
        (dim_store.write.format("delta").mode("overwrite").option("path", dim_store_path).option("overwriteSchema", "true").saveAsTable("retail_sales_db.dim_store"))

        spark.sql("DROP TABLE IF EXISTS retail_sales_db.dim_product")
        (dim_product.write.format("delta").mode("overwrite").option("path", dim_product_path).option("overwriteSchema", "true").saveAsTable("retail_sales_db.dim_product"))

        spark.sql("DROP TABLE IF EXISTS retail_sales_db.fact_sales")
        (fact_sales.write.format("delta").mode("overwrite").option("path", fact_sales_path).option("overwriteSchema", "true").saveAsTable("retail_sales_db.fact_sales"))

    except Exception as e:
        print(f"Error in bronze to silver transformation: {e}")
        spark.stop()
        raise

    print("Bronze to Silver transformation completed successfully.")
    spark.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PySpark Bronze to Silver ETL Job")
    parser.add_argument("--dim_customer_output_path", required=True, help="S3A output path for DimCustomer")
    parser.add_argument("--dim_store_output_path", required=True, help="S3A output path for DimStore")
    parser.add_argument("--dim_product_output_path", required=True, help="S3A output path for DimProduct")
    parser.add_argument("--fact_sales_output_path", required=True, help="S3A output path for FactSales")
    args = parser.parse_args()
    main(args.dim_customer_output_path, args.dim_store_output_path, args.dim_product_output_path, args.fact_sales_output_path)