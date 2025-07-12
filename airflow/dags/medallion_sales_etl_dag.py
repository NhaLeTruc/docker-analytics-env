from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os
from include.custom_utils.minio_utils import ensure_bucket_exists

# Get MinIO credentials from environment variables
MINIO_SPARK_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SPARK_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 31)
}

dag = DAG(
    'sales_medallion_etl',
    default_args=default_args,
    catchup=False
)

# Ensure MinIO bucket exists
ensure_bucket = PythonOperator(
    task_id='ensure_bucket_exists',
    python_callable=ensure_bucket_exists,
    op_kwargs={'bucket_name': 'mybucket'},
    dag=dag
)

# Bronze ingestion task
bronze_ingestion = SparkSubmitOperator(
    task_id='bronze_ingestion',
    application='dags/bronze_ingestion.py',
    conn_id='spark_default',
    conf={
        "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
        "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
        "spark.hadoop.fs.s3a.access.key": MINIO_SPARK_ACCESS_KEY,
        "spark.hadoop.fs.s3a.secret.key": MINIO_SPARK_SECRET_KEY,
        "spark.hadoop.fs.s3a.path.style.access": "true",
        "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
        "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider"
    },
    application_args=['--output_path', 's3a://mybucket/retails_sales_db/bronze/raw_data'],
    dag=dag
)

# Bronze to Silver transformation task
bronze_to_silver = SparkSubmitOperator(
    task_id='bronze_to_silver',
    application='dags/bronze_to_silver.py',
    conn_id='spark_default',
    conf={
        "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
        "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
        "spark.hadoop.fs.s3a.access.key": MINIO_SPARK_ACCESS_KEY,
        "spark.hadoop.fs.s3a.secret.key": MINIO_SPARK_SECRET_KEY,
        "spark.hadoop.fs.s3a.path.style.access": "true",
        "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
        "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider"
    },
    application_args=["--dim_customer_output_path", 's3a://mybucket/retails_sales_db/silver/dim_customer',
                      "--dim_store_output_path", 's3a://mybucket/retails_sales_db/silver/dim_store',
                      "--dim_product_output_path", 's3a://mybucket/retails_sales_db/silver/dim_product',
                      "--fact_sales_output_path", 's3a://mybucket/retails_sales_db/silver/fact_sales'],
    dag=dag
)

# Silver to Gold transformation task
silver_to_gold = SparkSubmitOperator(
    task_id='silver_to_gold',
    application='dags/silver_to_gold.py',
    conn_id='spark_default',
    conf={
        "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
        "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
        "spark.hadoop.fs.s3a.access.key": MINIO_SPARK_ACCESS_KEY,
        "spark.hadoop.fs.s3a.secret.key": MINIO_SPARK_SECRET_KEY,
        "spark.hadoop.fs.s3a.path.style.access": "true",
        "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
        "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider"
    },
    application_args=['--output_path', 's3a://mybucket/retails_sales_db/gold/gold_sales_summary'],
    dag=dag
)

# task dependencies
ensure_bucket >> bronze_ingestion >> bronze_to_silver >> silver_to_gold

