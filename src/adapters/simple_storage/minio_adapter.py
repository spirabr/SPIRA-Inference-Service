from io import BytesIO
import os
from typing import Tuple
from minio import Minio


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

    def store_inference_file(
        self, inference_id: str, file_type: str, file_extension: str, raw_file: BytesIO
    ):
        """stores the file in minIO server

        Args:
            inference_id (dict) : inference id
            file_type (str) : type of the file being stored
            file_extension (dict) : file extension
            raw_file (BytesIO) : file stream

        Returns:
            None

        """
        length = raw_file.getbuffer().nbytes
        self._client.put_object(
            self._bucket_name,
            inference_id + os.sep + file_type + file_extension,
            raw_file,
            length,
        )

    def get_inference_file(self, inference_id: str, filename: str) -> Tuple[bytes, str]:
        """gets the file in minIO server

        Args:
            inference_id (dict) : inference id
            filename (str) : name of the file being stored

        Returns:
            tuple containing file content as byte array and string containing file extension

        """
        response = self._client.get_object(
            self._bucket_name,
            inference_id + os.sep + filename + self._default_extension,
        )
        try:
            return (
                response.data,
                self._default_extension,
            )
        finally:
            response.close()
            response.release_conn()
