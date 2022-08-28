import pytest
from src.adapters.model_register.mlflow_adapter import MLFlowAdapter
from src.core.model.inference import Inference, InferenceFiles, UploadAudio
from src.core.model.result import ResultUpdate

from tests.mocks.mlflow_mock import MLFlowMock


@pytest.fixture
def adapter_instance():

    adapter = MLFlowMock()

    return adapter


def test_predict_method(adapter_instance: MLFlowAdapter):
    inference = Inference(
        **{
            "id": "629f815d6abaa3c5e6cf7c16",
            "sex": "M",
            "age": 23,
            "rgh": "fake_rgh",
            "covid_status": "Sim",
            "mask_type": "None",
            "user_id": "507f191e810c19729de860ea",
            "model_id": "629f992d45cda830033cf4cd",
            "status": "processing",
            "created_in": "2022-07-18 17:07:16.954632",
        },
    )
    vogal_sustentada = open("tests/mocks/audio_files/audio1.wav", "rb")
    parlenda_ritmada = open("tests/mocks/audio_files/audio2.wav", "rb")
    frase = open("tests/mocks/audio_files/audio3.wav", "rb")
    aceite = open("tests/mocks/audio_files/audio4.wav", "rb")

    inference_files = InferenceFiles(
        aceite=UploadAudio(content=aceite.read(), filename="aceite.wav"),
        vogal_sustentada=UploadAudio(
            content=vogal_sustentada.read(), filename="vogal_sustentada.wav"
        ),
        parlenda_ritmada=UploadAudio(
            content=parlenda_ritmada.read(), filename="parlenda_ritmada.wav"
        ),
        frase=UploadAudio(content=frase.read(), filename="frase.wav"),
    )

    output, diagnosis = adapter_instance.predict(
        inference,
        inference_files,
    )
    assert output == [0.1, 0.2, 0.4]
    assert diagnosis == "negative"
