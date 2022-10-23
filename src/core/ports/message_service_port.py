import json
from core.model.inference import Inference
from core.model.message_service import RequestLetter

from core.model.result import ResultUpdate


class MessageServicePort:
    """Port for the message service

    Args:
        message_service_adapter (Adapter Class) : message service adapter instance

    """

    def __init__(self, message_service_adapter):
        self._message_service_adapter = message_service_adapter

    async def send_message(self, letter: RequestLetter):
        """sends a serialized json to the message service

        Args:
            letter (RequestLetter) : object containing message and publishing channel

        Returns:
            None

        """
        await self._message_service_adapter.send_message(
            json.dumps(letter.content.dict()), letter.publishing_channel
        )

    async def subscribe(self, receiving_channel: str):
        """subscribes to the channel to receive messages from it

        Args:
            receiving_channel (str) : receiving channel

        Returns:
            None

        """
        await self._message_service_adapter.subscribe(receiving_channel)

    async def wait_for_message(self, receiving_channel: str) -> Inference:
        """waits until a message arrives in the given channel from the message service

        Args:
            receiving_channel (str) : channel to listen

        Returns:
            result update form

        """
        # message_dict = json.loads(
        #     await self._message_service_adapter.wait_for_message(receiving_channel)
        # )
        FAKE_INFERENCE_WITH_ID_1 = {
            "id": "629f815d6abaa3c5e6cf7c16",
            "gender": "M",
            "age": 23,
            "rgh": "fake_rgh",
            "covid_status": "Sim",
            "mask_type": "None",
            "user_id": "507f191e810c19729de860ea",
            "model_id": "629f992d45cda830033cf4cd",
            "status": "processing",
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
        return Inference(**FAKE_INFERENCE_WITH_ID_1)
