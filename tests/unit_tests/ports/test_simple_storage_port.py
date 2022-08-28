from io import BytesIO
from mock import ANY, MagicMock, patch
import pytest
from core.model.inference import UploadAudio
from core.ports.simple_storage_port import SimpleStoragePort

from tests.mocks.minio_mock import MinioMock

adapter_instance = MinioMock()


@pytest.fixture()
def simple_storage_port():
    port = SimpleStoragePort(adapter_instance)
    return port


def test_get_inference_file(simple_storage_port: SimpleStoragePort):
    file = BytesIO(open("tests/mocks/audio_files/audio1.wav", "rb").read())

    def get_inference_file(inference_id, filename) -> None:
        return file.getvalue(), ".an_extension"

    with patch.object(
        adapter_instance,
        "get_inference_file",
        MagicMock(side_effect=get_inference_file),
    ) as mock_method:
        ret = simple_storage_port.get_inference_file(
            "fake_inference_id", "fake_filename"
        )

        mock_method.assert_called_once_with("fake_inference_id", "fake_filename")

        assert ret == UploadAudio(
            content=file.getvalue(),
            filename="fake_filename" + ".an_extension",
        )
