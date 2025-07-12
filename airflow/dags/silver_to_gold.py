from pyspark.sql import SparkSession
from pyspark.sql import functions as f
import argparse

def main(gold_output_path):
    # Create Spark session
    spark = (SparkSession.builder
        .appName("SilverToGold")
        .config("hive.metastore.uris", "thrift://hive-metastore:9083")
        .enableHiveSupport()
        .getOrCreate())

    print("Silver to Gold: Spark session created.")

    try:
        # Read clean dimension and fact tables from the Silver layer
        dim_customer = spark.table("retail_sales_db.dim_customer")
        dim_store = spark.table("retail_sales_db.dim_store")
        dim_product = spark.table("retail_sales_db.dim_product")
        # For performance, limit the fact table as requested.
        fact_sales = spark.table("retail_sales_db.fact_sales").limit(10000)
        print("Successfully read clean tables from Silver layer (limited to 10000 sales facts).")

        # --- Gold Layer Transformation (Enrichment and Aggregation) ---
        
        # Data Privacy Check: By joining and then aggregating without selecting PII columns
        # (e.g., customer_name, customer_email), we ensure sensitive data is not exposed in the final Gold table.
        sales_enriched = (
            fact_sales.alias("f")
            .join(f.broadcast(dim_customer.alias("c")), "customer_id", "inner")
            .join(f.broadcast(dim_store.alias("s")), "store_id", "inner")
            .join(f.broadcast(dim_product.alias("p")), "product_id", "inner")
            .withColumn("transaction_date", f.to_date("transaction_timestamp"))
        )

        gold_df = (
            sales_enriched
            .groupBy("transaction_date", "s.store_name", "p.product_category")
            .agg(
                f.sum("total_amount").alias("total_sales"),
                f.sum("quantity").alias("units_sold"),
                f.countDistinct("transaction_id").alias("num_transactions")
            )
            .withColumn("processing_date", f.current_date())
        )
        
        # --- Gold Layer Data Quality Checks (Validity & Consistency) ---
        # Filter out any unreasonable aggregated values that are not positive.
        gold_df_validated = gold_df.filter(
            (f.col("total_sales") > 0) &
            (f.col("units_sold") > 0)
        )
        
        print(f"Aggregated data created. Writing {gold_df_validated.count()} validated records to Gold layer.")

        # Write aggregated data to Gold table
        spark.sql("DROP TABLE IF EXISTS retail_sales_db.gold_sales_summary")
        (gold_df_validated.write.format("delta")
            .mode("overwrite")
            .option("path", gold_output_path)
            .option('overwriteSchema', 'true')
            .saveAsTable("retail_sales_db.gold_sales_summary"))
        
    except Exception as e:
        print(f"Error in Silver to Gold transformation: {e}")
        spark.stop()
        raise

    print("Silver to Gold transformation completed successfully.")
    spark.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PySpark Silver to Gold ETL Job")
    parser.add_argument("--output_path", required=True, help="S3A output path for Gold data")
    args = parser.parse_args()
    main(args.output_path)