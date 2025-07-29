# Lakehouse Template

Template for typical data engineer's local development works. Containerized local environments for data transfers / transforms / queries / visualizations. This project aims at delivering a standardized local infrastructure for individual data engineer's workstation. It would allow development and testing of data engineering projects completely under one's control.

## Components

1. Apache Spark & Livy & Iceberg
2. Nessie Catalog
3. Minio
4. Postgres
5. PgAdmin4
6. JupyterLab & SparkMagic
7. Apache Superset

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

curl -X POST -H "Content-Type: application/json" -d '{"kind": "spark"}' http://localhost:8998/sessions
curl http://localhost:8998/sessions/{sessionId}
curl -X POST -H "Content-Type: application/json" -d '{"code": "1 + 1"}' http://localhost:8998/sessions/{sessionId}/statements
curl -X POST -H "Content-Type: application/json" -d '{"file": "/path/to/your/spark_app.jar", "className": "com.example.MySparkApp"}' http://localhost:8998/batches

sudo docker cp f3be49b69438:/opt/bitnami/zeppelin/logs/zeppelin-defaultuser-f3be49b69438.out ./
```
