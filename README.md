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

## Getting Started

```bash
sudo docker compose up -d
```

## Why Spark Thrift?

It is the service which provides a flavour of server-client (jdbc/odbc)Facility with spark. Server Client facility means we don’t need the spark to be installed in our machine .Instead we will be a client and we will be given a server url to which we can connect and use the data with our application for example in our use case we will using Pyhive Client to connect to spark ecosystem started in some server machine. Connect spark table and queries with apps written in Java Python etc without starting a spark application.

In short Spark Thrift is a JDBC/ODBC interface for executing SQL queries on Spark dedicated server from non-Spark applications.

## Spark Thrift Server versus Apache Livy

While both Spark Thrift Server and Apache Livy enable remote access to Spark, they serve different purposes. Spark Thrift Server provides a JDBC/ODBC interface for executing SQL queries on Spark, while Apache Livy offers a REST API for submitting and managing Spark jobs and interactive sessions. Livy is more versatile, supporting various languages and job types, while Spark Thrift Server is specialized for SQL-based access.

However, Livy is still in the incubation phase at the Apache Software Foundation (ASF). This means it's not yet fully endorsed by the ASF.

## Apache Kyuubi

Kyuubi acts as a gateway, providing a unified SQL interface (Thrift JDBC/ODBC) to different engines like Spark and Flink. It's designed for multiple users and workloads, allowing for efficient resource utilization. Kyuubi supports load balancing and high availability through ZooKeeper, enabling it to handle a large number of concurrent clients and diverse workloads. Kyuubi integrates with Kerberos and LDAP for authentication and authorization. Kyuubi aims to simplify access to data processing engines, making it easier for users to leverage the power of Spark, Flink, etc., without needing to directly interact with them.

Is short Kyuubi is a data engines gateway with some proxy capacities built in for handling client applications interactions with engines.

## Apache Kyuubi REST API

The Apache Kyuubi REST API provides a way to interact with Kyuubi using HTTP requests, primarily for batch operations and for scenarios where short-lived connections are preferred. It offers a different approach compared to the Thrift binary protocol, which is typically used for interactive sessions with long-lived connections. The REST API is built on short HTTP connections and is particularly useful in high-availability deployments where multiple Kyuubi instances are behind a load balancer.

### Batch Operations and Short-lived Connections

The REST API is designed for tasks that don't require a persistent connection, making it suitable for batch processing and situations where a quick exchange of information is needed.

### High Availability and Load Balancing

In a distributed setup, the REST API allows requests to be routed to different Kyuubi instances through a load balancer, ensuring high availability and fault tolerance.

### Integration with Other Systems

The REST API enables integration with other systems and applications that can communicate over HTTP, expanding Kyuubi's reach and usability.

### Complementary to Thrift

While the Thrift binary protocol is used for interactive sessions, the REST API provides a different interface for specific use cases, offering flexibility in how users interact with Kyuubi.

### SQL Dialect Support

Kyuubi's REST API supports various SQL dialects, including Hive and Spark, allowing users to interact with data sources in a familiar manner.

### Multi-Tenancy and Resource Management

Kyuubi leverages the REST API to manage multi-tenancy and resource allocation, enabling efficient sharing and isolation of resources within a cluster.

### Data Lake/Lakehouse Support

The REST API, along with other Kyuubi features, contributes to the platform's vision of becoming a unified data lake management solution, supporting various data formats and workloads.

### Ease of Use

End-users can utilize the REST API, along with JDBC and SQL, to explore data in a serverless manner, simplifying the process of data discovery and analysis
