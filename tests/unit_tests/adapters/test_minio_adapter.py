from io import BytesIO
from typing import Iterable
from mock import ANY, MagicMock, patch
from pydantic import BaseModel
import pytest
from adapters.simple_storage.minio_adapter import MinioAdapter
from tests.mocks.minio_mock import MinioMock
from minio.deleteobjects import DeleteObject


@pytest.fixture()
def simple_storage_adapter():
    adapter = MinioMock()
    return adapter


def test_store_inference_file(simple_storage_adapter: MinioAdapter):
    def fake_put_object(bucket_name: str, file_name: str, file: BytesIO, length):
        pass

    with patch.object(
        simple_storage_adapter._client,
        "put_object",
        MagicMock(side_effect=fake_put_object),
    ) as mock_method:
        file = BytesIO(open("tests/mocks/audio_files/audio1.wav", "rb").read())
        try:
            simple_storage_adapter.store_inference_file(
                "fake_inference_id",
                "fake_file_type",
                ".fake_extension",
                file,
            )
            assert True
        except:
            assert False
        mock_method.assert_called_once_with(
            "mock-bucket",
            "fake_inference_id/fake_file_type.fake_extension",
            ANY,
            565292,
        )


def test_get_inference_file(simple_storage_adapter: MinioAdapter):
    file = BytesIO(open("tests/mocks/audio_files/audio1.wav", "rb").read())

    class FakeResponse:
        def __init__(self):
            self.data = file.getvalue()

        def release_conn(self):
            pass

        def close(self):
            pass

    mock_response = FakeResponse()

    mock_response.release_conn = MagicMock()

    mock_response.close = MagicMock()

    def fake_get_object(bucket_name: str, file_name: str):
        return mock_response

    with patch.object(
        simple_storage_adapter._client,
        "get_object",
        MagicMock(side_effect=fake_get_object),
    ) as mock_method:

        try:
            content, extension = simple_storage_adapter.get_inference_file(
                "fake_inference_id", "fake_file_type"
            )
            assert content == file.getvalue()
            assert extension == ".fake_extension"
        except:
            assert False

        mock_method.assert_called_once_with(
            "mock-bucket", "fake_inference_id/fake_file_type.fake_extension"
        )
        mock_response.release_conn.assert_called_once()
        mock_response.close.assert_called_once()
