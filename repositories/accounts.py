"""Repositories module."""

import models.documents
from application_context import AppContext
from . base import BaseRepository
class AccountsRepository(BaseRepository):

    def __init__(self,session_factory,app_context:AppContext) -> None:
        BaseRepository.__init__(self,session_factory,app_context)
        self.session_factory = session_factory

    async def update_password(self, user_id, hash_pass:str):
        models.documents.Users._id == user_id
        ret = await self.db_context.update_one_async(
            models.documents.Users,
            models.documents.Users._id ==user_id,
            (
                models.documents.Users.HashPassword==hash_pass
            )
        )
        return ret
