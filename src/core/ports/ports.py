from core.ports.message_service_port import MessageServicePort
from core.ports.simple_storage_port import SimpleStoragePort


class Ports:
    """Object to store the project ports

    Args:
        message_service_port (MessageServicePort) : message service port instance
        simple_storage_port (SimpleStoragePort) : simple storage port instance
    """

    def __init__(
        self,
        message_service_port: MessageServicePort,
        simple_storage_port: SimpleStoragePort,
    ):
        self.message_service_port = message_service_port
        self.simple_storage_port = simple_storage_port
