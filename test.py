import syncer

from webapp.database import DbConnection
from dependency_injector import containers, providers
from webapp.services.users import UserService
from dependency_injector.wiring import Provide,inject
from repositories import UserRepository
from application_context import AppContext

class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yml"])

    app_context = providers.Factory(
        AppContext
    )
    db_connection = providers.Factory(
        DbConnection,
        db_config=config.db,
        app_context=app_context
    )
    user_repository = providers.Factory(
            UserRepository,
            session_factory=db_connection.provided.session,
            app_context= app_context

        )


    user_service = providers.Factory(
        UserService,
        user_repository
    )

    print(config)

fx= Container()

@inject
def test(user_service:UserService= Provide[Container.user_service],u2:UserService= Provide[Container.user_service]):
    async def run():
        users=await user_service.get_users()
        print(users)
        for x in users:
            print(x)
    syncer.sync(run())
container = Container()
container.init_resources()
container.wire(modules=[__name__])

test()