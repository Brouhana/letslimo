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

    if is_base64:
        body = base64.b64decode(body)

    s3resource.Bucket(
        OBJECT_STORAGE_BUCKET).put_object(Key=key, Body=body, ACL='public-read', ContentType='image/jpeg')

    object_url = 'https://{0}.{1}.cdn.digitaloceanspaces.com/{2}'.format(
        OBJECT_STORAGE_BUCKET, OBJECT_STORAGE_REGION, key)

    return object_url
