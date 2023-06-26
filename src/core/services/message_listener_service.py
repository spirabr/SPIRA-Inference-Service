import logging
from urllib import response
from core.model.exception import LogicException
from core.model.inference import Inference, InferenceFiles
from core.model.message_service import RequestLetter
from core.model.result import ResultUpdate
from core.ports.message_service_port import MessageServicePort
from core.ports.model_register_port import ModelRegisterPort
from core.ports.simple_storage_port import SimpleStoragePort

logging.basicConfig(level = logging.INFO)

async def subscribe_to_channel(
    message_service_port: MessageServicePort,
    channel: str,
) -> None:
    """subscribes the listener service to a channel in the message service

    Args:
        message_service_port (MessageServicePort) : message service port
        channel (str) : channel to subscribe in

    Returns:
        None

    Raises:
        exception, if there was an error subscribing

    """
    try:
        await message_service_port.subscribe(channel)
    except:
        raise LogicException("cound not subscribe to channel")


async def listen_for_messages_and_respond(
    simple_storage_port: SimpleStoragePort,
    message_service_port: MessageServicePort,
    model_register_port: ModelRegisterPort,
    receiving_channel: str,
    responding_channel: str,
) -> None:
    """waits for a message to arrive at the receiving channel in message service
        and return the prediction

    Args:
        simple_storage_port (SimpleStoragePort) : simple storage port
        message_service_port (MessageServicePort) : message service port
        model_register_port (ModelRegisterPort) : model register port instance
        receiving_channel (str) : inference requests channel
        responding_channel (str) : channel in which prediction is returned

    Returns:
        None

    Raises:
        exception, if there was an error waiting for messages
        exception, if there was an error getting the files from the simple storage
        exception, if there was an error while sending the response

    """
    try:
        logging.info("waiting for inference on channel {}.".format(receiving_channel))
        inference: Inference = await message_service_port.wait_for_message(
            receiving_channel
        )
        logging.info("inference received: {}".format(inference))
        inference_files: InferenceFiles = _get_files(
            simple_storage_port, inference
        )
        logging.info("audios received.")
        logging.info("attempting to perform prediction...")
        result_update: ResultUpdate = model_register_port.predict(
            inference, inference_files
        )
        logging.info("prediction complete.")
        logging.info(result_update)
        await message_service_port.send_message(
            RequestLetter(content=result_update, publishing_channel=responding_channel)
        )

    except LogicException:
        raise
    except Exception as e:
        logging.error(e)
        raise LogicException("an error occurred while waiting for the messages")


def _get_files(
    simple_storage_port: SimpleStoragePort, inference: Inference
) -> InferenceFiles:
    """gets the files form the inference stored by the api service

    Args:
        simple_storage_port (SimpleStoragePort) : simple storage port
        inference (Inference) : inference object

    Returns:
        object containing the inference files as UploadAudio attributes

    Raises:
        exception, if there was an error while retrieving the files

    """
    try:
        files = {}
        file_types = InferenceFiles.__fields__.keys()
        for file_type in file_types:
            files[file_type] = simple_storage_port.get_inference_file(inference.id, file_type)

        return InferenceFiles(**files)
    except Exception as e:
        logging.error(e)
        raise LogicException("cound not update inference result")
