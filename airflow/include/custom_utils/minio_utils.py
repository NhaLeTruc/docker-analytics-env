from minio import Minio
from minio.error import S3Error
import os

MINIO_ENDPOINT = "minio:9000"


def ensure_bucket_exists(bucket_name):
    
    minio_access_key = os.getenv("MINIO_ACCESS_KEY")
    minio_secret_key = os.getenv("MINIO_SECRET_KEY")

    if not minio_access_key or not minio_secret_key:
        print("Error: MINIO_ACCESS_KEY or MINIO_SECRET_KEY environment variables not set.")
        raise ValueError("MinIO access/secret key not found in environment variables.")

    client = Minio(
        MINIO_ENDPOINT,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False
    )
    try:
        found = client.bucket_exists(bucket_name)
        if not found:
            print(f"Bucket '{bucket_name}' not found. Creating it...")
            client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        else:
            print(f"Bucket '{bucket_name}' already exists.")
        return True
    
    except S3Error as exc:
        print(f"Error checking or creating bucket '{bucket_name}': {exc}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred with bucket '{bucket_name}': {e}")
        raise

if __name__ == '__main__':

    try:
        ensure_bucket_exists("test-bucket-from-util")
    except Exception as e:
        print(f"Failed: {e}") 