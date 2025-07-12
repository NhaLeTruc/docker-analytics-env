#!/bin/bash

export HADOOP_CLASSPATH=${HADOOP_HOME}/share/hadoop/tools/lib/*:${HADOOP_CLASSPATH}

# Substitute environment variables in hive-site.xml
# Define the list of variables to be substituted
export HIVE_SITE_VARS='${MARIADB_USER} ${MARIADB_PASSWORD} ${MINIO_ACCESS_KEY} ${MINIO_SECRET_KEY}'
cat /opt/hive/conf/hive-site.xml | envsubst "$HIVE_SITE_VARS" > /opt/hive/conf/hive-site.xml.tmp && mv /opt/hive/conf/hive-site.xml.tmp /opt/hive/conf/hive-site.xml

# Wait for MariaDB
while ! nc -z mariadb 3306; do
  echo "Waiting for MariaDB to be ready..."
  sleep 1
done

# Initialize the metastore schema
$HIVE_HOME/bin/schematool -dbType mysql -initSchema

# Start the metastore
$HIVE_HOME/bin/hive --service metastore 