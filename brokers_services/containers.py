"""Containers module."""
import os.path
import pathlib

from dependency_injector import containers, providers
#
from services.logger_services import LoggerService
from repositories.kafka_consumers.files_uploaded import ConsumerFileUploaded
from repositories.base_message import BaseMessage, FakeMessage
from repositories.kafka_message import KafkaMessageRepository
from repositories.s3_repository import FileStorageS3DbRepository
# from services.message import MessageServices
from repositories.file_storage_base import FileStorageBaseRepository
from repositories.file_storage_mongo import FileStorageMongoDbRepository
# from repositories.files import FileRepository
from repositories.apps import AppContext


class FileProcessingContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[

        "__main__"

    ])

    config = providers.Configuration(yaml_files=["config.yml"])

    config.load()
    app_context: AppContext = providers.Factory(
        AppContext,
        config=config
    )

    logger_service: LoggerService =providers.Factory(
        LoggerService,
        working_dir = str(pathlib.Path(__file__).parent)

    )
    file_storage_repo: FileStorageBaseRepository = None
    msg_repo: BaseMessage = providers.Factory(
        FakeMessage
    )
    if config.get('storage').get('type') == 's3':
        file_storage_repo: FileStorageBaseRepository = providers.Factory(
            FileStorageS3DbRepository,
            app_context=app_context,
            config=config
        )
    if config.get('storage').get('type') == 'mongodb':
        file_storage_repo: FileStorageBaseRepository = providers.Factory(
            FileStorageMongoDbRepository,
            app_context=app_context,
            config=config
        )
    if config.get('storage').get('type') == 'file':
        file_storage_repo: FileStorageBaseRepository = providers.Factory(
            FileStorageMongoDbRepository,
            app_context=app_context,
            config=config
        )

    consumer_file_uploaded:ConsumerFileUploaded= providers.Factory(
        ConsumerFileUploaded,
        config=config,
        logger=logger_service
    )

    # if config.get('message').get('type') == 'kafka':
    #     msg_repo = providers.Factory(
    #         KafkaMessageRepository,
    #         config=config.get('message').get('kafka'),
    #         tmp_data_dir=config.get('message').get('temp-dir')
    #     )



