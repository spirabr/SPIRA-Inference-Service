from typing import List, Tuple
from unittest.mock import MagicMock, patch
import pytest
from core.model.inference import Inference, InferenceFiles, UploadAudio
from core.model.result import ResultUpdate

from src.core.ports.model_register_port import ModelRegisterPort
from tests.mocks.mlflow_mock import MLFlowMock

adapter_instance = MLFlowMock()


@pytest.fixture()
def model_register_port():
    port = ModelRegisterPort(adapter_instance)
    return port


def test_predict(model_register_port: ModelRegisterPort):
    def fake_predict(
        inference: Inference, inference_files: InferenceFiles
    ) -> Tuple[List[float], str]:
        return [0.1, 0.2, 0.3], "positive"

    with patch.object(
        adapter_instance,
        "predict",
        MagicMock(side_effect=fake_predict),
    ) as mock_method:
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
        result = model_register_port.predict(inference, inference_files)

        mock_method.assert_called_once_with(inference, inference_files)
        assert result == ResultUpdate(
            inference_id="629f815d6abaa3c5e6cf7c16",
            output=[0.1, 0.2, 0.3],
            diagnosis="positive",
        )
