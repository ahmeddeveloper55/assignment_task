import oss2
from django.core.files.storage import Storage
from django.conf import settings


class AliyunBaseStorage(Storage):
    """Base storage class for Alibaba OSS"""

    def __init__(self, location):
        self.location = location
        self.bucket_name = settings.ALIYUN_OSS_BUCKET_NAME
        self.endpoint = settings.ALIYUN_OSS_ENDPOINT
        self.access_key_id = settings.ALIYUN_OSS_ACCESS_KEY_ID
        self.access_key_secret = settings.ALIYUN_OSS_ACCESS_KEY_SECRET

        # Initialize OSS bucket connection
        self.bucket = oss2.Bucket(
            oss2.Auth(self.access_key_id, self.access_key_secret),
            f"https://{self.endpoint}",
            self.bucket_name,
        )

    def _get_full_path(self, name):
        """Get full path for a file in OSS"""
        return f"{self.location}/{name}"

    def _save(self, name, content):
        """Save file to OSS"""
        path = self._get_full_path(name)
        self.bucket.put_object(path, content.read())
        return name

    def _open(self, name, mode='rb'):
        """Retrieve file from OSS"""
        path = self._get_full_path(name)
        return self.bucket.get_object(path)

    def url(self, name):
        """Generate file URL"""
        return f"https://{self.bucket_name}.{self.endpoint}/{self._get_full_path(name)}"

    def exists(self, name):
        """Check if file exists"""
        path = self._get_full_path(name)
        try:
            self.bucket.get_object_meta(path)
            return True
        except oss2.exceptions.NoSuchKey:
            return False

    def delete(self, name):
        """Delete file from OSS"""
        path = self._get_full_path(name)
        try:
            self.bucket.delete_object(path)
        except oss2.exceptions.NoSuchKey:
            pass  # File does not exist, no need to raise an error


class StaticStorage(AliyunBaseStorage):
    """Storage backend for static files"""
    def __init__(self):
        super().__init__(location=settings.ALIYUN_STATIC_LOCATION)


class MediaStorage(AliyunBaseStorage):
    """Storage backend for media files"""
    def __init__(self):
        super().__init__(location=settings.ALIYUN_MEDIA_LOCATION)