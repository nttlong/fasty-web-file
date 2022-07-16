"""Services module."""

from uuid import uuid4
from typing import Iterator

from ..repositories.users  import UserRepository
from models.Model_Users import User
from typing import TypeVar, Generic
from .base import BaseService
class UserService(BaseService):

    def __init__(self, user_repository: UserRepository) -> None:
        BaseService.__init__(self)
        self._repository: UserRepository = user_repository
    def get_users(self) -> Iterator[User]:
        return self._repository.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        return self._repository.get_by_id(user_id)

    def create_user(self) -> User:
        uid = uuid4()
        return self._repository.add(email=f"{uid}@email.com", password="pwd")

    def delete_user_by_id(self, user_id: int) -> None:
        return self._repository.delete_by_id(user_id)

    async def get_user_by_name(self, username):
        return await self._repository.get_user_by_name(username)
