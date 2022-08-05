from core.ports.message_service_port import MessageServicePort
from core.ports.model_register_port import ModelRegisterPort
from core.ports.simple_storage_port import SimpleStoragePort


class Ports:
    """Object to store the project ports

    Args:
        message_service_port (MessageServicePort) : message service port instance
        simple_storage_port (SimpleStoragePort) : simple storage port instance
        model_register_port (ModelRegisterPort) : model register port instance
    """

    def __init__(
        self,
        message_service_port: MessageServicePort,
        simple_storage_port: SimpleStoragePort,
        model_register_port: ModelRegisterPort,
    ):
        self.message_service_port = message_service_port
        self.simple_storage_port = simple_storage_port
        self.model_register_port = model_register_port
