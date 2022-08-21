import json
from mock import ANY, MagicMock, patch
from core.model.message_service import RequestLetter
from core.model.result import ResultUpdate
from core.ports.message_service_port import MessageServicePort
from src.core.model.inference import Inference
from tests.mocks.nats_mock import NATSMock
import pytest
import asyncio

adapter_instance = NATSMock()


@pytest.fixture()
def message_service_port():
    port = MessageServicePort(adapter_instance)
    return port


def test_send_message(message_service_port: MessageServicePort):
    async def fake_send_message(topic: str, message: bytes):
        pass

    with patch.object(
        adapter_instance,
        "send_message",
        MagicMock(side_effect=fake_send_message),
    ) as mock_method:
        asyncio.run(
            message_service_port.send_message(
                RequestLetter(
                    content=ResultUpdate(
                        inference_id="fake_id", output=0.1, diagnosis="fake_diagnosis"
                    ),
                    publishing_channel="fake_topic",
                ),
            )
        )
        mock_method.assert_called_once_with(
            json.dumps(
                {
                    "inference_id": "fake_id",
                    "output": 0.1,
                    "diagnosis": "fake_diagnosis",
                }
            ),
            "fake_topic",
        )


def test_subscribe(message_service_port: MessageServicePort):
    async def fake_subscribe(topic: str):
        pass

    with patch.object(
        adapter_instance,
        "subscribe",
        MagicMock(side_effect=fake_subscribe),
    ) as mock_method:
        asyncio.run(message_service_port.subscribe("fake_topic"))
        mock_method.assert_called_once_with("fake_topic")


def test_wait_for_message(message_service_port: MessageServicePort):
    async def fake_wait_for_message(topic: str):
        return json.dumps(
            {
                "rgh": "fake_rgh",
                "age": 30,
                "sex": "M",
                "covid_status": "Sim",
                "mask_type": "None",
                "model_id": "fake_model_id",
                "status": "fake_status",
                "user_id": "fake_user_id",
                "created_in": "2022-07-18 17:07:16.954632",
                "id": "fake_inference_id",
            }
        )

    with patch.object(
        adapter_instance,
        "wait_for_message",
        MagicMock(side_effect=fake_wait_for_message),
    ) as mock_method:
        return_value = asyncio.run(message_service_port.wait_for_message("fake_topic"))
        assert return_value == Inference(
            **{
                "rgh": "fake_rgh",
                "age": 30,
                "sex": "M",
                "covid_status": "Sim",
                "mask_type": "None",
                "model_id": "fake_model_id",
                "status": "fake_status",
                "user_id": "fake_user_id",
                "created_in": "2022-07-18 17:07:16.954632",
                "id": "fake_inference_id",
            }
        )
