"""Repositories module."""
import datetime
import uuid

import bson.objectid

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

    async def get_sso_id(self, app_name, username, token, return_url_after_signIn):
        db_name=self.app_context.get_db_name('admin')
        if db_name is None:
            return None
        sso_info = models.documents.SSO({})
        sso_info.ReturnUrlAfterSignIn =return_url_after_signIn
        sso_info.Token =token
        sso_info.SSOID = str(uuid.uuid4())
        sso_info.CreatedOn=datetime.datetime.utcnow()
        sso_info.Application = app_name
        sso_info.Username = username
        sso_info._id= bson.objectid.ObjectId()
        await self.db_context(db_name).insert_one_async(
            models.documents.SSO_Info,
            sso_info.DICT
        )
        return sso_info.SSOID
    async def get_access_token_from_sso_id(self, SSOID):
        db_name = self.app_context.get_db_name('admin')
        ret = await self.db_context(db_name).find_one_async(
            models.documents.SSO_Info,
            models.documents.SSO_Info.SSOID==SSOID
        )
        if ret is None:
            return None
        return ret.Token

