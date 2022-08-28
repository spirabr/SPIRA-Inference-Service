from io import BytesIO
import os
import pytest
from adapters.simple_storage.minio_adapter import MinioAdapter
from settings import Settings
from minio.deleteobjects import DeleteObject
from minio import Minio


@pytest.fixture()
def simple_storage_adapter():
    adapter = MinioAdapter(
        Settings.simple_storage_settings.minio_conn_url,
        Settings.simple_storage_settings.minio_access_key,
        Settings.simple_storage_settings.minio_secret_key,
        "test-bucket",
        ".fake_extension",
    )
    yield adapter

    minio_client = Minio(
        Settings.simple_storage_settings.minio_conn_url,
        access_key=Settings.simple_storage_settings.minio_access_key,
        secret_key=Settings.simple_storage_settings.minio_secret_key,
        secure=False,
    )

    if minio_client.bucket_exists("test-bucket"):
        delete_object_list = map(
            lambda x: DeleteObject(x.object_name),
            minio_client.list_objects("test-bucket", recursive=True),
        )
        errors = minio_client.remove_objects("test-bucket", delete_object_list)
        for error in errors:
            print("error occured when deleting object", error, flush=True)
        minio_client.remove_bucket("test-bucket")


def test_store_inference_file(simple_storage_adapter: MinioAdapter):
    file = BytesIO(open("tests/mocks/audio_files/audio1.wav", "rb").read())
    simple_storage_adapter.store_inference_file(
        "fake_inference_id",
        "fake_file_type",
        ".fake_extension",
        file,
    )

    minio_client = Minio(
        Settings.simple_storage_settings.minio_conn_url,
        access_key=Settings.simple_storage_settings.minio_access_key,
        secret_key=Settings.simple_storage_settings.minio_secret_key,
        secure=False,
    )

    response = minio_client.get_object(
        "test-bucket",
        "fake_inference_id" + os.sep + "fake_file_type" + ".fake_extension",
    )

    assert response != None
    assert response.data == file.getvalue()

    response.close()
    response.release_conn()

    del minio_client


def test_get_inference_file(simple_storage_adapter: MinioAdapter):
    file = BytesIO(open("tests/mocks/audio_files/audio1.wav", "rb").read())
    simple_storage_adapter.store_inference_file(
        "fake_inference_id",
        "fake_file_type",
        ".fake_extension",
        file,
    )

    content, extension = simple_storage_adapter.get_inference_file(
        "fake_inference_id", "fake_file_type"
    )

    assert content == file.getvalue()
    assert extension == ".fake_extension"
