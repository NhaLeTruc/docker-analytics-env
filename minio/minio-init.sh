#!/bin/sh
minio server /bitnami/minio/data --console-address ':9001' & sleep 5;
mc alias set myminio http://localhost:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD};
mc admin accesskey create myminio/ --access-key ${MINIO_ACCESS_KEY} --secret-key ${MINIO_SECRET_KEY};
mc mb myminio/dummy;
mc mb myminio/datalake;
mc mb myminio/datalakehouse;
mc mb myminio/warehouse;
mc cp -r /dummy/* myminio/dummy/;
tail -f /dev/null