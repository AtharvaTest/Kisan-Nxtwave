from minio import Minio
from minio.error import S3Error
from app.config import settings

class StorageService:
    def __init__(self):
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )
        self.bucket = settings.minio_bucket
        self._ensure_bucket()

    def _ensure_bucket(self):
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
        except S3Error:
            pass

    def upload_bytes(self, key: str, data: bytes, content_type: str = "application/octet-stream"):
        import io
        self.client.put_object(self.bucket, key, io.BytesIO(data), len(data), content_type=content_type)

    def presigned_get(self, key: str):
        return self.client.presigned_get_object(self.bucket, key)

storage_service = StorageService()
