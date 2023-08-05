from urllib.parse import urlparse
import boto3

from .StorageStrategy import StorageStrategy

S3 = boto3.resource('s3')


class S3Storage(StorageStrategy):

    def __init__(self, boto_client=S3):
        super().__init__()
        self.client = boto_client

    def _read(self, path):

        return self._read_s3(path).read().decode('utf-8')

    def _read_as_chunk(self, path, chunk_size):
        s3_content = self._read_s3(path)
        while True:
            chunk = s3_content.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break

    def _read_s3(self, path):
        s3_path_info = urlparse(path)
        bucket = s3_path_info.netloc
        key = s3_path_info.path[1:]
        s3_object = self.client.Object(bucket, key)
        return s3_object.get()['Body']
