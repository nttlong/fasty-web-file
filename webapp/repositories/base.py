"""Repositories module."""

from contextlib import AbstractContextManager
from typing import Callable, Iterator
from ReCompact.db_async import DbContext
from  models.Model_Users import User
from ..contex import AppContext
class BaseRepository:
    def __init__(self,session_factory) -> None:

        self.session_factory = session_factory

    @property
    def db_context(self)->DbContext:
        ret= self.session_factory()
        return ret



class NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class UserNotFoundError(NotFoundError):

    entity_name: str = "User"