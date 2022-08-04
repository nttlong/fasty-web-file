from typing import TypeVar
from dependency_injector.wiring import inject
from dependency_injector import providers
from database_connector.database import DbConnection
T = TypeVar('T')

def get_repository(cls: T,db_name) -> T:   # Generic function
    db_connection = providers.Singleton(DbConnection)
    ret_provider = providers.Factory(
        T,
        session_factory=db_connection.provided.session,
    )
    ret = inject(ret_provider.cls)(db_connection.provided.session)
    ret.set_db(db_name)
    return ret