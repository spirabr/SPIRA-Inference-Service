from io import BytesIO
import os

from core.model.inference import UploadAudio


class SimpleStoragePort:
    """Port for the simple storage adapter

    Args:
        simple_storage_adapter (Adapter Class) : simple storage adapter instance

    """

    def __init__(self, simple_storage_adapter):
        self._simples_storage_adapter = simple_storage_adapter

    def get_inference_file(self, inference_id: str, filename: str) -> UploadAudio:
        """gets the upload_audio in minIO server

        Args:
            inference_id (dict) : inference id
            filename (str) : name of the file without extension

        Returns:
            UploadAudio

        """
        content, extension = self._simples_storage_adapter.get_inference_file(
            inference_id, filename
        )
        return UploadAudio(
            content=content,
            filename=filename + extension,
        )
