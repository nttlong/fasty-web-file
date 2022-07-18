"""Containers module."""
import os.path

from dependency_injector import containers, providers

from .database import DbConnection
from .repositories.users import UserRepository
from .services.users import UserService
from .contex import AppContext
from fastapi.templating import Jinja2Templates
class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    config = providers.Configuration(yaml_files=["config.yml"])
    config.load()
    templates_dir = config.get('front-end').get('server-templates')
    if not os.path.isdir(templates_dir):
        raise Exception(f"{templates_dir} was not found")
    templates = Jinja2Templates(directory=templates_dir)
    app_context = providers.Factory(
        AppContext
    )
    db = providers.Factory(
        DbConnection,

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
