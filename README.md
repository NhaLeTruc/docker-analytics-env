# Lakehouse Template

Template for typical data engineer's local development works. Containerized local environments for data transfers / transforms / queries / visualizations. This project aims at delivering a standardized local infrastructure for individual data engineer's workstation. It would allow development and testing of data engineering projects completely under one's control.

## Components

1. Apache Spark
2. Apache Spark Thrift
3. Nessie Catalog
4. Minio
5. Apache Iceberg
6. Postgres - backend only
7. PgAdmin4
8. JupyterLab
9. Apache Superset
10. Data Quality Ops

## Getting Started

```bash
sudo docker compose up -d

sudo watch docker ps -a

sudo watch docker images -a

sudo docker stop $(sudo docker ps -qa)

sudo docker start $(sudo docker ps -qa)

sudo docker rmi -f $(sudo docker images --filter=reference='data_quality_in_*' -qa)

sudo docker images --format "{{.ID}}\t{{.Size}}\t{{.Repository}}:{{.Tag}}" | sort -k 2 -h

sudo docker exec -it <CONTAINER_ID> bash

sudo docker inspect <CONTAINER_ID> | grep "IPAddress"

sudo docker compose up --build --no-deps --force-recreate

sudo docker compose down --volumes --remove-orphans

sudo docker compose down -rmi all

jupyter kernelspec list

cat /etc/os-release
```
