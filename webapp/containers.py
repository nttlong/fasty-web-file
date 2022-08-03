"""Containers module."""
import os.path
import pathlib

from dependency_injector import containers, providers

from repositories.base_message import BaseMessage, FakeMessage
from repositories.kafka_message import KafkaMessageRepository
from repositories.s3_repository import FileStorageS3DbRepository
from services.logger_services import LoggerService
from services.message import MessageServices
from .database import DbConnection
from repositories.apps import AppRepository
from repositories.file_storage_base import FileStorageBaseRepository
from repositories.file_storage_mongo import FileStorageMongoDbRepository
from repositories.files import FileRepository
from repositories.users import UserRepository
from repositories.accounts import AccountsRepository
from services.apps import AppService
from services.file_storage import FileStorageService
from services.files import FileService
from services.users import UserService
from services.accounts import AccountsService
from fastapi.templating import Jinja2Templates

from application_context import AppContext



class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "application",
        "endpoints",
        "utils",
        "__main__"
    ])

    config = providers.Configuration(yaml_files=["config.yml"])

    config.load()

    templates_dir = config.get('front-end').get('server-templates')
    if not os.path.isdir(templates_dir):
        raise Exception(f"{templates_dir} was not found")
    templates = providers.Singleton(
        Jinja2Templates,
        directory=templates_dir
    )
    app_context: AppContext = providers.Factory(
        AppContext,
        config=config
    )
    db = providers.Factory(
        DbConnection,

        app_context=app_context,
        db_config=config.db
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
        app_context=app_context

    )
    account_repository = providers.Factory(
        AccountsRepository,
        session_factory=db.provided.session,
        app_context=app_context
    )
    app_repository = providers.Factory(
        AppRepository,
        session_factory=db.provided.session,
        app_context=app_context
    )
    file_repository: FileRepository = providers.Factory(
        FileRepository,
        session_factory=db.provided.session,
        app_context=app_context
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

    if config.get('message').get('type') == 'kafka':
        msg_repo = providers.Factory(
            KafkaMessageRepository,
            config=config.get('message').get('kafka'),
            tmp_data_dir=config.get('message').get('temp-dir')
        )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    accounts_service = providers.Factory(
        AccountsService,
        account_repository=account_repository,
        config=config

    )
    apps_services = providers.Factory(
        AppService,
        app_repository=app_repository,
        app_context=app_context,
        config=config
    )
    file_service = providers.Factory(
        FileService,
        file_repository=file_repository
    )
    file_storage_service = providers.Factory(
        FileStorageService,
        file_storage_repository=file_storage_repo
    )
    message_service = providers.Factory(
        MessageServices,
        msg_repo=msg_repo
    )
