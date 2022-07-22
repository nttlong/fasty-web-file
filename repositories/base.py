"""Repositories module."""

from ReCompact.db_async import DbContext
from application_context import AppContext
class BaseRepository:
    def __init__(self,session_factory,app_context:AppContext) -> None:
        self.app_context:AppContext = app_context
        self.session_factory = session_factory


    def db_context(self,db_name)->DbContext:
        ret= self.session_factory(db_name)
        return ret



class NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class UserNotFoundError(NotFoundError):

    entity_name: str = "User"