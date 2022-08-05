from adapters.listener.message_listener import run_listener
from adapters.message_service.nats_adapter import NATSAdapter
from core.ports.message_service_port import MessageServicePort
from core.ports.model_register_port import ModelRegisterPort
from core.ports.ports import Ports
from core.ports.simple_storage_port import SimpleStoragePort
from settings import Settings


def configure_ports() -> Ports:
    """Instantiates Ports and Adapters of the services used in the application

    Args:
        None

    Returns:
        Ports object with port instances as attributes

    """
    ports = Ports(
        MessageServicePort(
            NATSAdapter(
                Settings.message_service_settings.nats_conn_url,
            )
        ),
        SimpleStoragePort(),
        ModelRegisterPort(),
    )
    return ports


if __name__ == "__main__":
    ports = configure_ports()
    print("starting listener process...", flush=True)
    run_listener(ports)
