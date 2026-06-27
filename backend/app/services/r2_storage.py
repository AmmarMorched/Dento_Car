import boto3
import uuid
import mimetypes
from botocore.config import Config
from app.core.config import settings


def _get_client():
    return boto3.client(
        "s3",
        endpoint_url=f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.R2_ACCESS_KEY,
        aws_secret_access_key=settings.R2_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )


def upload_image(image_bytes: bytes, folder: str = "originals", filename: str = None) -> str:
    """
    Upload raw image bytes to R2.
    Returns the public URL of the uploaded file.
    """
    client = _get_client()

    if not filename:
        filename = f"{uuid.uuid4().hex}.jpg"

    key = f"{folder}/{filename}"

    client.put_object(
        Bucket=settings.R2_BUCKET,
        Key=key,
        Body=image_bytes,
        ContentType="image/jpeg",
    )

    return f"{settings.R2_PUBLIC_URL}/{key}"


def upload_file(file_bytes: bytes, folder: str, filename: str, content_type: str = None) -> str:
    """
    Generic file upload (for PDFs, annotated images, etc).
    Returns the public URL.
    """
    client = _get_client()

    if not content_type:
        content_type, _ = mimetypes.guess_type(filename)
        content_type = content_type or "application/octet-stream"

    key = f"{folder}/{filename}"

    client.put_object(
        Bucket=settings.R2_BUCKET,
        Key=key,
        Body=file_bytes,
        ContentType=content_type,
    )

    return f"{settings.R2_PUBLIC_URL}/{key}"


def delete_file(key: str) -> None:
    """Delete a file from R2 by its key (e.g. 'originals/abc123.jpg')."""
    client = _get_client()
    client.delete_object(Bucket=settings.R2_BUCKET, Key=key)


def get_presigned_url(key: str, expires_in: int = 3600) -> str:
    """
    Generate a temporary signed URL for private files.
    expires_in: seconds (default 1 hour)
    """
    client = _get_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.R2_BUCKET, "Key": key},
        ExpiresIn=expires_in,
    )