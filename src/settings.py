from pydantic import BaseSettings


class MessageServiceSettings(BaseSettings):
    """Settings holding the environment variables for the NATSAdapter

    Attributes:
        nats_conn_url (str) : connection url to NATS server container

    """

    nats_conn_url: str


class MessageListenerSettings(BaseSettings):
    """Settings holding the environment variables for the message listener process

    Attributes:
        loop_interval (float) : time interval between loop iterations
        receiving_channel (str) : message service channel used to receive inference requests
        central_channel (str) : message service channel used to send inference responses
    """

    loop_interval: float
    receiving_channel: str
    central_channel: str


class SimpleStorageSettings(BaseSettings):
    """Settings holding the environment variables for the MinioAdapter

    Attributes:
        minio_conn_url (str) : connection url to minIO server container
        bucket_name (str) : name of the bucket used by the app
        minio_access_key (str) : minio access credentials
        minio_secret_key (str) : minio credentials

    """

    minio_conn_url: str
    bucket_name: str
    minio_access_key: str
    minio_secret_key: str


class Settings:
    """Settings gathering the environment variables for all adapters

    Attributes:
        database_settings (DatabaseSettings) : database settings object
        authentication_settings (AuthenticationSettings) : authentication settings object
        message_service_settings (MessageServiceSettings) : message_service settings object
        message_listener_settings (MessageListenerSettings) : message_listener settings object
        simple_storage_settings (SimpleStorageSettings) : simple_storage settings object

    """

    message_service_settings = MessageServiceSettings(
        _env_file="message_service.env", _env_file_encoding="utf-8"
    )

    message_listener_settings = MessageListenerSettings(
        _env_file="message_listener.env", _env_file_encoding="utf-8"
    )

    simple_storage_settings = SimpleStorageSettings(
        _env_file="simple_storage.env", _env_file_encoding="utf-8"
    )
