from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime
from airflow.operators.dummy import DummyOperator
import os

# Get MinIO credentials from environment variables
MINIO_SPARK_ACCESS_KEY = os.getenv('MINIO_ROOT_USER', 'minioadmin')
MINIO_SPARK_SECRET_KEY = os.getenv('MINIO_ROOT_PASSWORD', 'minioadmin')

dag =  DAG(
    dag_id="export_dq_results_to_minio",
    start_date=datetime(2025, 5, 31),
    schedule_interval="@daily"
)
start_task = DummyOperator(
    task_id="start_task",
    dag=dag
)

export_dq_task = SparkSubmitOperator(
        task_id="export_dq_results_to_minio",
        application="/opt/airflow/dags/export_dq_results.py",
        conn_id="spark_default", # This connection should be configured in Airflow UI for Spark Master
        conf={
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.access.key": MINIO_SPARK_ACCESS_KEY,
            "spark.hadoop.fs.s3a.secret.key": MINIO_SPARK_SECRET_KEY,
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension", # Re-adding Delta Lake config
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog", # Re-adding Delta Lake config
        },
        application_args=[
            "--target_minio_path", "s3a://dqopsbucket/dqops_results/", # Target MinIO bucket and path where data will be stored
            "--target_table_name", "dqops_results" # Name of the external Hive table
        ],
    )

end_task = DummyOperator(   
    task_id="end_task",
    dag=dag
)

start_task >> export_dq_task >> end_task