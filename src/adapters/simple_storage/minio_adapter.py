from io import BytesIO
import os
from minio import Minio
from minio.deleteobjects import DeleteObject


class MinioAdapter:
    """Adapter for the minIO server

    Args:
        minio_conn_url (str) : connection url to minIO server container
        bucket_name (str) : name of the bucket used by the app
        minio_access_key (str) : minio access credentials
        minio_secret_key (str) : minio credentials
        default_extension (str) : default file extension in storage

    """

    def __init__(
        self,
        conn_url: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        default_extension: str,
    ):
        self._default_extension = default_extension
        self._client = Minio(
            conn_url, access_key=access_key, secret_key=secret_key, secure=False
        )
        self._bucket_name = bucket_name
        if not self._client.bucket_exists(bucket_name):
            self._client.make_bucket(bucket_name)

    def get_inference_file(self, inference_id: str, filename: str):
        """gets the file in minIO server

        Args:
            inference_id (dict) : inference id
            filename (str) : name of the file being stored

        Returns:
            None

        """
        return (
            self._client.get_object(
                self._bucket_name,
                inference_id + os.sep + filename + self._default_extension,
            ),
            self._default_extension,
        )
