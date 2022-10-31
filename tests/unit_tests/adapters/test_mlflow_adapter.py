import pytest
from src.adapters.model_register.mlflow_adapter import MLFlowAdapter
from src.core.model.inference import Inference, InferenceFiles, UploadAudio
from src.core.model.result import ResultUpdate

from tests.mocks.mlflow_mock import MLFlowMock

INFERENCE_JSON_1_WITH_ID = {
    "id": "fake_inference_id",
    "gender": "M",
    "age": 23,
    "rgh": "fake_rgh",
    "covid_status": "Sim",
    "mask_type": "None",
    "user_id": "507f191e810c19729de860ea",
    "model_id": "629f994245cda830033cf4cf",
    "status": "processing",
    "local": "hospital_1",
    "cid": "fake_cid",
    "bpm": "fake_bpm",
    "created_in": "2022-07-18 17:07:16.954632",
    "respiratory_frequency": "123",
    "respiratory_insufficiency_status": "Sim",
    "location": "h1",
    "last_positive_diagnose_date": "",
    "hospitalized": "TRUE",
    "hospitalization_start": "2022-07-18 17:07:16.954632",
    "hospitalization_end": "2022-07-18 17:07:16.954632",
    "spo2": "123",
}

@pytest.fixture
def adapter_instance():

    adapter = MLFlowMock()

    return adapter


def test_predict_method(adapter_instance: MLFlowAdapter):
    inference = Inference(
        **INFERENCE_JSON_1_WITH_ID,
    )
    sustentada = open("tests/mocks/audio_files/audio1.wav", "rb")
    parlenda = open("tests/mocks/audio_files/audio2.wav", "rb")
    frase = open("tests/mocks/audio_files/audio3.wav", "rb")
    aceite = open("tests/mocks/audio_files/audio4.wav", "rb")

    inference_files = InferenceFiles(
        aceite=UploadAudio(content=aceite.read(), filename="aceite.wav"),
        sustentada=UploadAudio(
            content=sustentada.read(), filename="sustentada.wav"
        ),
        parlenda=UploadAudio(
            content=parlenda.read(), filename="parlenda.wav"
        ),
        frase=UploadAudio(content=frase.read(), filename="frase.wav"),
    )

    output, diagnosis = adapter_instance.predict(
        inference,
        inference_files,
    )
    assert output == [0.1, 0.2, 0.4]
    assert diagnosis == "negative"
