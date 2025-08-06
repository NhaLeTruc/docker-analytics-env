# Lakehouse Template

Template for typical data engineer's local development works. Containerized local environments for data transfers / transforms / queries / visualizations. This project aims at delivering a standardized local infrastructure for individual data engineer's workstation. It would allow development and testing of data engineering projects completely under one's control.

## Components

1. Apache Spark & Iceberg
2. JupyterLab & Toree
3. Minio
4. Nessie Catalog
5. Apache Superset
6. Postgres & PgAdmin4

## Getting Started

```bash
# Deploy docker compose environment
make up

# Shut down docker compose environment
make down
```
