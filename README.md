# Lakehouse Template

Template for typical data engineer's local development works. Containerized local environments for data transfers / transforms / queries / visualizations. This project aims at delivering a standardized local infrastructure for individual data engineer's workstation. It would allow development and testing of data engineering projects completely under one's control.

## Components

1. Apache Spark
2. Apache Spark Streaming
3. Apache Spark Thrift
4. Apache Hive
5. Minio
6. Apache Iceberg
7. Apache Trino

## Why Spark Thrift?

It is the service which provides a flavour of server-client (jdbc/odbc)Facility with spark. Server Client facility means we don’t need the spark to be installed in our machine .Instead we will be a client and we will be given a server url to which we can connect and use the data with our application for example in our use case we will using Pyhive Client to connect to spark ecosystem started in some server machine. Connect spark table and queries with apps written in Java Python etc without starting a spark application.

In short Spark Thrift is a JDBC/ODBC interface for executing SQL queries on Spark dedicated server from non-Spark applications.

## Getting Started

```bash
sudo docker compose up -d
```
