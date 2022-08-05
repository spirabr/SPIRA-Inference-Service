from adapters.listener.message_listener import run_listener
from adapters.message_service.nats_adapter import NATSAdapter
from adapters.simple_storage.minio_adapter import MinioAdapter
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
        SimpleStoragePort(
            MinioAdapter(
                Settings.simple_storage_settings.minio_conn_url,
                Settings.simple_storage_settings.minio_access_key,
                Settings.simple_storage_settings.minio_secret_key,
                Settings.simple_storage_settings.bucket_name,
                Settings.simple_storage_settings.default_extension,
            )
        ),
        ModelRegisterPort(),
    )
    return ports


if __name__ == "__main__":
    ports = configure_ports()
    print("starting listener process...", flush=True)
    run_listener(ports)
