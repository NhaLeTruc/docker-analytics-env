from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, IntegerType, DateType, TimestampType
from pyspark.sql import functions as f
from pyspark.sql.window import Window
import argparse

def main(output_path_arg):
    # Create Spark session with MinIO S3A configs
    spark = (SparkSession.builder
        .appName("BronzeIngestion")
        .config("hive.metastore.uris", "thrift://hive-metastore:9083")
        .enableHiveSupport()
        .getOrCreate())

    print("Bronze Ingestion: Spark session created.")

    # Define schema explicitly
    schema = StructType([
        StructField("transaction_id",         LongType(),     False),
        StructField("transaction_timestamp",  StringType(),False),
        StructField("quantity",               StringType(),  True),
        StructField("unit_price",             DoubleType(),   False),
        StructField("total_amount",           DoubleType(),   False),
        StructField("payment_method",         StringType(),   True),

        StructField("customer_id",            DoubleType(),     True),
        StructField("customer_name",          StringType(),   True),
        StructField("customer_gender",        StringType(),   True),
        StructField("customer_dob",           StringType(),     True),
        StructField("customer_email",         StringType(),   True),
        StructField("customer_phone",         LongType(),   True),
        StructField("customer_city",          StringType(),   True),
        StructField("customer_state",         StringType(),   True),

        StructField("store_id",               DoubleType(),  True),
        StructField("store_name",             StringType(),   True),
        StructField("store_city",             StringType(),   True),
        StructField("store_state",            StringType(),   True),

        StructField("product_id",             DoubleType(),  True),
        StructField("product_name",           StringType(),   True),
        StructField("product_category",       StringType(),   True)
    ])

    # Load data
    local_parquet_path = "/opt/airflow/data/very_dirty_data.parquet"

    try:
        df = spark.read.schema(schema).parquet(local_parquet_path)
        print(f"Successfully loaded customers data from: {local_parquet_path}")

        spark.sql("DROP TABLE IF EXISTS retail_sales_db.dirty_data")
        (df.write.format("delta")
            .mode("overwrite")
            .option("path", 's3a://mybucket/retails_sales_db/dirty_data')
            .option("overwriteSchema", "true")
            .saveAsTable("retail_sales_db.dirty_data"))
        # --- Bronze Layer Data Quality Checks ---

        # Validity
        df_casted = df.withColumn("transaction_timestamp", f.to_timestamp(f.col("transaction_timestamp"))) \
            .withColumn("quantity", f.col("quantity").cast(IntegerType())) \
            .withColumn("customer_id", f.col("customer_id").cast(LongType())) \
            .withColumn("customer_dob", f.to_date(f.col("customer_dob"))) \
            .withColumn("customer_phone", f.col("customer_phone").cast(StringType())) \
            .withColumn("store_id", f.col("store_id").cast(LongType())) \
            .withColumn("product_id", f.col("product_id").cast(LongType()))

        # 1. Completeness
        df_no_nulls = df_casted.dropna()
        
        # 2. Validity
        email_regex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
        df_validated = df_no_nulls.filter(f.to_date(f.col("transaction_timestamp")).isNotNull()) \
            .filter(f.col("customer_email").rlike(email_regex)) \
            .filter(f.col("quantity") >= 0) \
            .filter(f.col("total_amount") >= 0) \
            .filter(f.col("unit_price") >= 0) \
            .filter(f.col("transaction_timestamp") < f.current_timestamp())

        # Clean product_category
        df_validated = df_validated.withColumn("product_category", f.trim(f.lower(f.col("product_category"))))
        df_validated = df_validated.withColumn("product_category",
            f.when(f.col("product_category") == "boks", "books")
             .when(f.col("product_category") == "hom", "home")
             .when(f.col("product_category") == "elctronics", "electronics")
             .when(f.col("product_category") == "cloting", "clothing")
             .otherwise(f.col("product_category"))
        )
        df_validated = df_validated.withColumn("product_category", f.initcap(f.col("product_category")))

        # 3. Uniqueness
        window_spec = Window.partitionBy("transaction_id").orderBy(f.col("transaction_timestamp").asc())
        df_cleaned = df_validated.withColumn("row_num", f.row_number().over(window_spec)) \
                                 .filter(f.col("row_num") == 1) \
                                 .drop("row_num")

        print(f"Applied Bronze DQ checks. Original count: {df.count()}, Cleaned count: {df_cleaned.count()}")

    except Exception as e:
        print(f"Error loading parquet file or applying initial DQ checks: {e}")
        spark.stop()
        raise

    try:
        # Create database if it doesn't exist
        spark.sql("CREATE DATABASE IF NOT EXISTS retail_sales_db")

        # Write data to Minio and register in Hive Metastore
        spark.sql("DROP TABLE IF EXISTS retail_sales_db.raw_data")
        
        (df_cleaned.write.format("delta")
            .mode("overwrite")
            .option("path", output_path_arg)
            .option("overwriteSchema", "true")
            .saveAsTable("retail_sales_db.raw_data"))
            
        print(f"Successfully wrote and registered table retail_sales_db.raw_data at {output_path_arg}")

    except Exception as e:
        print(f"Error writing data to Minio/Hive: {e}")
        spark.stop()
        raise

    print("Bronze ingestion job completed successfully.")
    spark.stop()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="...")
    parser.add_argument("--output_path", required=True, help="...")
    args = parser.parse_args()

    main(args.output_path)
