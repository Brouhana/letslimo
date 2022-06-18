import boto3
import os
import base64


OBJECT_STORAGE_REGION = 'nyc3'
ACCESS_KEY_ID = os.environ.get('DO_SPACES_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.environ.get('DO_SPACES_SECRET_ACCESS_KEY')
OBJECT_STORAGE_BUCKET = 'letslimo'

s3config = {
    "region_name": OBJECT_STORAGE_REGION,
    "endpoint_url": "https://{}.digitaloceanspaces.com".format(OBJECT_STORAGE_REGION),
    "aws_access_key_id": ACCESS_KEY_ID,
    "aws_secret_access_key": SECRET_ACCESS_KEY}


def upload_file(key, body, is_base64):
    s3resource = boto3.resource("s3", **s3config)
    s3client = boto3.client("s3", **s3config)

    if is_base64:
        body = base64.b64decode(body)

    s3object = s3resource.Bucket(
        OBJECT_STORAGE_BUCKET).put_object(Key=key, Body=body, ContentType='image/jpeg')

    object_url = s3client.generate_presigned_url(
        "get_object",
        Params={"Bucket": OBJECT_STORAGE_BUCKET, "Key": s3object.key},
        ExpiresIn=60*60)

    return object_url
