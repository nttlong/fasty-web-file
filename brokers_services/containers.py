"""Containers module."""
import pathlib

from dependency_injector import containers, providers
#
from repositories.files import FileRepository
from repositories.kafka_consumers.message_file_thumb import ConsumerFileImageProcessThumb
from services.files import FileService
from services.logger_services import LoggerService
from repositories.kafka_consumers.files_uploaded import ConsumerFileUploaded
from repositories.base_message import BaseMessage, FakeMessage
from repositories.s3_repository import FileStorageS3DbRepository
# from services.message import MessageServices
from repositories.file_storage_base import FileStorageBaseRepository
from repositories.file_storage_mongo import FileStorageMongoDbRepository
# from repositories.files import FileRepository
from repositories.apps import AppContext
from database_connector.database import DbConnection
import start_config
class FileProcessingContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[

        "__main__"

    ])

    config = providers.Configuration(yaml_files=[start_config.get_config_path()])

    config.load()
    app_context: AppContext = providers.Factory(
        AppContext,
        config=config
    )

    logger_service: LoggerService =providers.Factory(
        LoggerService,
        working_dir = str(pathlib.Path(__file__).parent.parent)

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
    db = providers.Factory(
        DbConnection,

        app_context=app_context,
        db_config=config.db
    )
    file_repository: FileRepository = providers.Factory(
        FileRepository,
        session_factory=db.provided.session,
        app_context=app_context
    )
    file_service: FileService = providers.Factory(
        FileService,
        file_repository=file_repository
    )
    consumer_file_image_process_thumb:ConsumerFileImageProcessThumb = providers.Factory(
        ConsumerFileImageProcessThumb,
        config =config,
        logger=logger_service,
        file_storage_repo=file_storage_repo,
        file_service =file_service

    )





