import ReCompact
import models.documents
from .base import BaseRepository
from application_context import AppContext


class AppRepository(BaseRepository):

    def __init__(self, session_factory,app_context:AppContext) -> None:
        BaseRepository.__init__(self,session_factory,app_context)
        self.session_factory = session_factory

    async def get_all(self,app_name:str):
        agg = self.db_context(self.app_context.get_db_name(app_name)).aggregate(models.documents.Apps)
        agg.project(
            models.documents.Apps.Name,
            models.documents.Apps.Description,
            models.documents.Apps.RegisteredBy,
            ReCompact.dbm.FIELDS.AppId == models.documents.Apps._id
        ).sort(
            models.documents.Apps.RegisteredOn.desc(),
            models.documents.Apps.Name.asc()
        )
        ret = await agg.to_list_async()
        return ret

    async def get_app_by_name(self, app_name:str,app_name_to_get)->models.documents.Apps:
        return await self.db_context(self.app_context.get_db_name(app_name)).find_one_async(
            models.documents.Apps,
            models.documents.Apps.Name==app_name_to_get.lower()
        )

    async def create(self, app):
        db_name = self.app_context.get_db_name('admin')
        ret= await self.db_context(db_name).insert_one_async(
            models.documents.Apps,
            app.DICT
        )
        return ret