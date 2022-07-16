"""Containers module."""

from dependency_injector import containers, providers

from .database import DbConnection
from .repositories.users import UserRepository
from .services.users import UserService
from .contex import AppContext

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    config = providers.Configuration(yaml_files=["config.yml"])
    app_context = providers.Factory(
        AppContext
    )
    db = providers.Factory(DbConnection,
                             app_context= app_context,
                             db_config= config.db
                             )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,


    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )