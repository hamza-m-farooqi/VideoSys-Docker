import os
import uuid
import boto3
import requests as http_requests
import settings as settings


def webhook_response(webhook_url, status, code, message, data=None):
    response_data = {"status": status, "code": code, "message": message, "data": data}
    print(response_data)
    if webhook_url and "http" in webhook_url:
        http_requests.post(webhook_url, json=response_data)
    return None


def upload_to_s3(save_path):
    """
    Uploads an image to Amazon S3 and returns the object URL

    :param file_obj: File object to upload.
    :param bucket_name: Name of the bucket to upload to.
    :param object_path: Full path (including file name) inside the bucket.
    :return: URL of the uploaded object if successful, else None
    """
    object_path = f"open-sora/{str(uuid.uuid4())}.mp4"
    bucket_name = settings.AWS_BUCKET_NAME
    with open(save_path, "rb") as file_obj:

        session = boto3.session.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION,
        )
        bucket_url = settings.AWS_URL

        s3 = session.resource("s3")
        try:
            s3.Bucket(bucket_name).upload_fileobj(file_obj, object_path)
            # Construct the object URL
            object_url = f"{bucket_url}{object_path}"
            return object_url
        except Exception as e:
            print(e)
            return None


def download_file(url, save_directory="."):
    file_name = url.split("/")[-1]
    file_path = os.path.join(save_directory, file_name)
    response = http_requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return file_path
    else:
        raise Exception(f"Failed to download file: {response.status_code}")
