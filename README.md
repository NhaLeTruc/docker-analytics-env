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

## Spark Thrift Server versus Apache Livy

While both Spark Thrift Server and Apache Livy enable remote access to Spark, they serve different purposes. Spark Thrift Server provides a JDBC/ODBC interface for executing SQL queries on Spark, while Apache Livy offers a REST API for submitting and managing Spark jobs and interactive sessions. Livy is more versatile, supporting various languages and job types, while Spark Thrift Server is specialized for SQL-based access.

However, Livy is still in the incubation phase at the Apache Software Foundation (ASF). This means it's not yet fully endorsed by the ASF.

## Apache Kyuubi

Kyuubi acts as a gateway, providing a unified SQL interface (Thrift JDBC/ODBC) to different engines like Spark and Flink. It's designed for multiple users and workloads, allowing for efficient resource utilization. Kyuubi supports load balancing and high availability through ZooKeeper, enabling it to handle a large number of concurrent clients and diverse workloads. Kyuubi integrates with Kerberos and LDAP for authentication and authorization. Kyuubi aims to simplify access to data processing engines, making it easier for users to leverage the power of Spark, Flink, etc., without needing to directly interact with them.

Is short Kyuubi is a data engines gateway with some proxy capacities built in for handling client applications interactions

## Getting Started

```bash
sudo docker compose up -d
```
