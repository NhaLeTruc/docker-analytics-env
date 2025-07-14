# Data Quality in Lakehouse

This project implements a modern data lakehouse architecture using Docker for containerization. It demonstrates a full data lifecycle, from ingestion and processing to data quality monitoring and business intelligence.

## Architecture

The architecture is designed to be scalable, modular, and robust, leveraging open-source technologies.

<img width="1020" alt="Screenshot 2025-06-23 at 12 31 46" src="https://github.com/user-attachments/assets/2c8a1c55-0044-4515-b7dd-c48444aacfb8" />


The main components of the architecture are:

*   **Infrastructure (Docker):** The entire platform is containerized using Docker and managed with Docker Compose, ensuring portability and ease of deployment.
*   **Orchestration and Monitoring (Apache Airflow):** Airflow is used to schedule, orchestrate, and monitor the data pipelines. This includes ingestion, ETL jobs, and data quality checks.
*   **Object Storage (MinIO & Delta Lake):** MinIO provides an S3-compatible object storage solution. Delta Lake is used on top of MinIO to bring reliability, performance, and ACID transactions to the data lake. The storage is organized into three layers (Medallion Architecture):
    *   **Bronze:** Raw, unprocessed data ingested from source systems.
    *   **Silver:** Cleaned, validated, and enriched data.
    *   **Gold:** Aggregated data, ready for analytics and business intelligence.
*   **Metadata Management (Hive Metastore):** Hive Metastore stores the schema and metadata of the tables in the data lake, allowing Spark and other tools to have a centralized schema repository.
*   **Data Quality (DQOps):** DQOps is integrated to ensure data quality across the lakehouse. It connects to the Spark Thrift Server to retrieve schemas and run data quality checks using SQL.
*   **Query Engine (Spark Thrift Server):** The Spark Thrift Server provides a JDBC/ODBC interface to the data stored in the lakehouse, allowing BI tools to query the data using standard SQL.
*   **Analytics & BI (Apache Superset):** Superset is a modern data exploration and visualization platform. It connects to the Spark Thrift Server to query the gold layer data and build interactive dashboards.

## Data Flow

1.  **Ingestion:** Data is ingested from various sources into the Bronze layer in MinIO. This process is orchestrated by an Airflow DAG.
2.  **ETL Processing:** Airflow triggers Spark jobs to perform transformations:
    *   **Bronze to Silver:** Raw data is cleaned, deduplicated, and transformed.
    *   **Silver to Gold:** Silver data is aggregated and modeled to create business-level tables.
3.  **Data Quality:** DQOps continuously monitors the data in the lakehouse. It runs predefined checks and rules to detect anomalies, schema changes, and other data quality issues.
4.  **Analytics:** Business users and data analysts can explore the curated data in the Gold layer using Apache Superset, creating reports and dashboards to derive insights.

## Technology Stack

*   **Orchestration:** Apache Airflow
*   **Containerization:** Docker, Docker Compose
*   **Object Storage:** MinIO
*   **Data Lakehouse Format:** Delta Lake
*   **Compute Engine:** Apache Spark
*   **Metadata Store:** Hive Metastore
*   **Data Quality:** DQOps
*   **BI & Analytics:** Apache Superset

## How to Run

To start the platform, you can use the docker-compose files.

1.  **Start the main services (Spark, MinIO, Hive Metastore, etc.):**
    ```bash
    sudo docker compose up -d
    ```

2.  **Start Airflow services:**
    ```bash
    sudo docker compose -f docker-compose-airflow.yaml up -d
    ```

3. **Start All services:**
   ```bash
   sudo docker compose -f docker-compose-airflow.yaml -f docker-compose.yaml up -d
   ```

Please refer to the `docker-compose.yaml` and `docker-compose-airflow.yaml` for details on the services and their configurations.

## Project Structure

```
├── airflow/            # Airflow DAGs, plugins, and configurations
├── dqops_userhome/     # DQOps user home with checks, rules, and sources
├── hive/               # Hive Metastore configuration and Dockerfile
├── spark/              # Spark configuration and Dockerfile
├── superset/           # Superset configuration and Dockerfile
├── docker-compose.yaml # Main services for the data platform
├── docker-compose-airflow.yaml # Services for Airflow
└── README.md
```

## Demonstration

Here is a step-by-step demonstration of the data flow and data quality process within the lakehouse.

### 1. Medallion ETL Pipeline

The main ETL pipeline is orchestrated by Apache Airflow. This DAG, shown below, is responsible for ingesting raw data and processing it through the different layers of the Medallion architecture.

<img width="999" alt="Screenshot 2025-06-23 at 12 53 06" src="https://github.com/user-attachments/assets/da3252e9-fcfe-4c4e-a9e1-8cd3b86edbe5" />

The pipeline executes the following steps:
-   **`ensure_bucket_exists`**: A `PythonOperator` that creates the necessary MinIO buckets if they don't exist.
-   **`bronze_ingestion`**: A `SparkSubmitOperator` that ingests raw data into the Bronze layer.
-   **`bronze_to_silver`**: A `SparkSubmitOperator` that cleans and transforms the Bronze data, storing it in the Silver layer.
-   **`silver_to_gold`**: A `SparkSubmitOperator` that aggregates the Silver data into business-ready tables in the Gold layer.

### 2. Data Storage in MinIO

After the pipeline runs, the processed data is stored in MinIO, organized by the Medallion layers (Bronze, Silver, Gold). The image below shows the `retail_sales_db` inside the `mybucket` bucket, which contains the data for each layer.

<img width="1426" alt="Screenshot 2025-06-23 at 12 55 08" src="https://github.com/user-attachments/assets/4e5119e1-d39f-4b0f-b552-072ec1703f8d" />

### 3. Data Quality Profiling with DQOps

Data quality is a critical component of this architecture. DQOps is used to profile the data and run quality checks. The screenshot below shows the DQOps UI profiling the `dirty_data` table, providing statistics on total rows, column count, and detailed metrics for each column like null percentage and distinct value counts.

<img width="1726" alt="Screenshot 2025-06-23 at 12 56 40" src="https://github.com/user-attachments/assets/32d30c79-1f59-4904-a6de-93cbb6250e1f" />

### 4. Exporting Data Quality Results

To make the data quality results available for further analysis and reporting, another Airflow DAG is used to export them from DQOps. This DAG submits a Spark job (`export_dq_results_to_minio`) that extracts the results.

<img width="706" alt="Screenshot 2025-06-23 at 12 57 42" src="https://github.com/user-attachments/assets/e317da03-3bcc-4729-8fa3-0f111f81f6ff" />

### 5. DQ Results in MinIO

The exported data quality results are stored in a separate MinIO bucket named `dqopsbucket`. This keeps the DQ metrics separate from the primary data and makes them easy to access for reporting tools.

<img width="1594" alt="Screenshot 2025-06-23 at 12 58 23" src="https://github.com/user-attachments/assets/b2477fa8-a80a-4ac7-b415-9ca6e83d8efe" />

### 6. Visualizing Data Quality in Superset

Finally, the data quality results are visualized in an Apache Superset dashboard. This provides an intuitive and interactive way to monitor the quality of the data, with KPIs for different quality dimensions and charts showing the percentage of executed checks. This enables stakeholders to quickly assess data reliability.

<img width="1711" alt="Screenshot 2025-06-23 at 12 59 49" src="https://github.com/user-attachments/assets/17ee9319-aa1a-48d7-903d-4cc0463422bc" />
