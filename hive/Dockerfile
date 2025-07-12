FROM openjdk:8-jre-slim

ENV HADOOP_VERSION=3.3.6
ENV HIVE_VERSION=3.1.2
ENV MYSQL_CONNECTOR_VERSION=5.1.49


# Install required packages
RUN apt-get update && \
    apt-get install -y wget netcat procps gettext-base default-mysql-client gettext && \
    rm -rf /var/lib/apt/lists/*

# Download and extract Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xzf hadoop-${HADOOP_VERSION}.tar.gz && \
    mv hadoop-${HADOOP_VERSION} /opt/hadoop && \
    rm hadoop-${HADOOP_VERSION}.tar.gz && \
    # Remove conflicting SLF4J JAR from Hadoop
    rm -f /opt/hadoop/share/hadoop/common/lib/slf4j-reload4j-*.jar

# Download and extract Hive
RUN wget https://archive.apache.org/dist/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz && \
    tar -xzf apache-hive-${HIVE_VERSION}-bin.tar.gz && \
    mv apache-hive-${HIVE_VERSION}-bin /opt/hive && \
    rm apache-hive-${HIVE_VERSION}-bin.tar.gz

# Ensure Hive lib directory exists and download AWS/other Jars into Hive lib
RUN mkdir -p /opt/hive/lib && \
    wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.1/hadoop-aws-3.3.1.jar -P /opt/hive/lib/ && \
    wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.901/aws-java-sdk-bundle-1.11.901.jar -P /opt/hive/lib/ && \
    wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/${MYSQL_CONNECTOR_VERSION}/mysql-connector-java-${MYSQL_CONNECTOR_VERSION}.jar -P /opt/hive/lib/ && \
    # Ensure the Hive lib has the MySQL connector
    ls /opt/hive/lib/mysql-connector-java-*.jar

# Set environment variables
ENV HADOOP_HOME=/opt/hadoop
ENV HIVE_HOME=/opt/hive
ENV PATH=$PATH:${HADOOP_HOME}/bin:${HIVE_HOME}/bin
# Ensure Hive's SLF4J implementation is preferred if any conflicts remain
ENV HADOOP_USER_CLASSPATH_FIRST=true
ENV HIVE_USER_CLASSPATH_FIRST=true

# Create conf directory and copy configuration files
RUN mkdir -p /opt/hive/conf
COPY conf/* /opt/hive/conf
COPY entrypoint.sh /

RUN chmod +x /entrypoint.sh

EXPOSE 9083

ENTRYPOINT ["/entrypoint.sh"]