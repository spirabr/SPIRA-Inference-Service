from asyncio import sleep
import asyncio
from core.ports.ports import Ports

from core.services.message_listener_service import (
    listen_for_messages_and_update,
    subscribe_to_channel,
)
from settings import Settings


async def listen_for_messages_loop(
    message_service_port: MessageServicePort,
):
    """continuously listens for messages (inference requests) and processes the response

    Args:
        simple_storage_port (SimpleStoragePort) : port for simple storage
        message_service_port (MessageServicePort) : port for message service
        database_port (DatabasePort) : port for database

    Returns:
        None

    """
    try:
        await subscribe_to_channel(
            message_service_port, Settings.message_listener_settings.central_channel
        )
    except Exception as e:
        print(e, flush=True)

    while True:
        await sleep(Settings.message_listener_settings.loop_interval)
        try:
            await listen_for_messages_and_respond(
                simple_storage_port,
                message_service_port,
                database_port,
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
            ports.database_port,
        )
    )
