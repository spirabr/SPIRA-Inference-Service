from asyncio import sleep
import asyncio
from core.ports.message_service_port import MessageServicePort
from core.ports.model_register_port import ModelRegisterPort
from core.ports.ports import Ports
from core.ports.simple_storage_port import SimpleStoragePort
from core.services.message_listener_service import (
    listen_for_messages_and_respond,
    subscribe_to_channel,
)


from settings import Settings


async def listen_for_messages_loop(
    simple_storage_port: SimpleStoragePort,
    message_service_port: MessageServicePort,
    model_register_port: ModelRegisterPort,
):
    """continuously listens for messages (inference requests) and processes the response

    Args:
        simple_storage_port (SimpleStoragePort) : port for simple storage
        message_service_port (MessageServicePort) : port for message service
        model_register_port (ModelRegisterPort) : port for model register

    Returns:
        None

    """
    try:
        await subscribe_to_channel(
            message_service_port, Settings.message_listener_settings.receiving_channel
        )
    except Exception as e:
        print(e, flush=True)

    while True:
        await sleep(Settings.message_listener_settings.loop_interval)
        try:
            await listen_for_messages_and_respond(
                simple_storage_port,
                message_service_port,
                model_register_port,
                Settings.message_listener_settings.receiving_channel,
                Settings.message_listener_settings.central_channel,
            )
        except Exception as e:
            print(e, flush=True)


def run_listener(ports: Ports):
    """runs the listener process

    Args:
        ports (Ports) : ports object with all the instantiated ports

    Returns:
        None

    """
    asyncio.new_event_loop().run_until_complete(
        listen_for_messages_loop(
            ports.simple_storage_port,
            ports.message_service_port,
            ports.model_register_port,
        )
    )
