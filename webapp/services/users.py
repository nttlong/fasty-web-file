"""Services module."""

from uuid import uuid4
from typing import Iterator

from repositories.users import UserRepository
from models.Model_Users import User
from .base import BaseService
from application_context import AppContext


class UserService(BaseService):

    def __init__(self, user_repository: UserRepository) -> None:
        BaseService.__init__(self)
        self._repository: UserRepository = user_repository

    def get_users(self) -> Iterator[User]:
        return self._repository.get_all()

    async def get_user_by_id(self, user_id: int) -> User:
        return self._repository.get_by_id(user_id)

    async def create_user(self,app_name:str,user:User) -> User:
        return await self._repository.create_user(app_name,user)

    def delete_user_by_id(self, user_id: int) -> None:
        return self._repository.delete_by_id(user_id)

    async def get_user_by_name(self,app_name, username)->User:
        return await self._repository.get_user_by_name(app_name,username)
