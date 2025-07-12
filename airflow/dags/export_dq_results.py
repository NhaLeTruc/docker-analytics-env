from pyspark.sql import SparkSession
from pyspark.sql.functions import current_date, date_format
import sys
import os
import argparse

def main(target_minio_path, target_table_name):
    spark = (
        SparkSession.builder
        .appName("ExportDQOpsResultsToMinioAndHive")
        .config("hive.metastore.uris", "thrift://hive-metastore:9083")
        .enableHiveSupport()
        .getOrCreate()
    )
    print("Spark session created for exporting DQOps results to Minio and Hive.")

    # Hardcode the source path as per user request
    source_path = "/data/check_results"

    # Read all parquet files from the source path, Spark handles partitioning
    print(f"Reading DQOps results from: {source_path}")
    dq_results_df = spark.read.parquet(source_path)

    print(f"Writing consolidated DQOps results to MinIO and registering as Hive table: dqops.{target_table_name}")

    # Ensure the database exists, mimicking bronze_ingestion
    spark.sql("CREATE DATABASE IF NOT EXISTS dqops")

    # Drop the table if it exists, mimicking bronze_ingestion
    spark.sql(f"DROP TABLE IF EXISTS dqops.{target_table_name}")

    # Write the data to MinIO as a Delta table and register in Hive Metastore, mimicking bronze_ingestion
    (dq_results_df # Repartition to 1 to consolidate into a single file
        .write
        .format("delta") # Writing as Delta format
        .mode("overwrite")  # Overwrite the entire output path for this run
        .option("mergeSchema", "true")
        .option("path", target_minio_path) # Specify the external path
        .saveAsTable(f"dqops.{target_table_name}")) # Save as table

    print(f"Successfully exported consolidated DQOps results from {source_path} to {target_minio_path} and registered as dqops.{target_table_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export DQOps results to MinIO and register as an external Hive table.")
    parser.add_argument("--target_minio_path", type=str, required=True,
                        help="Base S3a path in MinIO to store consolidated DQOps results (e.g., s3a://mybucket/dqops_results/)")
    parser.add_argument("--target_table_name", type=str, required=True,
                        help="Name of the target external Hive table (e.g., dqops_results_external)")

    args = parser.parse_args()
    main(args.target_minio_path, args.target_table_name) 