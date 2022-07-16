"""Repositories module."""

from contextlib import AbstractContextManager
from typing import Callable, Iterator

import models.documents
from ReCompact.db_async import DbContext
from  models.Model_Users import User
from . base import BaseRepository
class UserRepository(BaseRepository):

    def __init__(self,session_factory) -> None:
        BaseRepository.__init__(self,session_factory)
        self.session_factory = session_factory
    async def get_all(self) -> Iterator[User]:
        return await self.db_context.find_async(
            docs= models.documents.Users,
            filter= {}
        )
    async def get_user_by_name(self, username):
        return await self.db_context.find_one_async(
            docs=models.documents.Users,
            filter=models.documents.Users.Username==username
        )
    def get_by_id(self, user_id: int) -> User:
        raise NotImplemented

    def add(self, email: str, password: str, is_active: bool = True) -> User:
        raise NotImplemented

    def delete_by_id(self, user_id: int) -> None:
        raise NotImplemented




class NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class UserNotFoundError(NotFoundError):

    entity_name: str = "User"