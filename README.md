# Lakehouse Template

Template for typical data engineer's local development works. Containerized local environments for data transfers / transforms / queries / visualizations. This project aims at delivering a standardized local infrastructure for individual data engineer's workstation. It would allow development and testing of data engineering projects completely under one's control.

## Components

1. Apache Spark
2. Apache Spark Thrift
3. Nessie Catalog
4. Minio
5. Apache Iceberg
6. Apache Airflow
7. Postgres - metadata only
8. JupyterLab
9. Apache Superset
10. Data Quality Ops

## Getting Started

```bash
sudo docker compose up -d
```
