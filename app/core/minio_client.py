import boto3
from botocore.client import Config
import uuid
import os

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "images")

session_boto = boto3.session.Session()
s3 = session_boto.client(
    service_name="s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)

def upload_image_to_minio(file):
    ext = file.filename.split(".")[-1]
    key = f"{uuid.uuid4()}.{ext}"

    s3.upload_fileobj(file.file, MINIO_BUCKET, key, ExtraArgs={"ContentType": file.content_type})

    url = f"http://localhost:9000/{MINIO_BUCKET}/{key}"
    return url


def delete_image_from_minio(url):
    key = url.split("/")[-1]
    try:
        s3.delete_object(Bucket=MINIO_BUCKET, Key=key)
    except Exception as e:
        print(f"Erreur lors de la suppression de l'image {key} : {e}")
        raise e