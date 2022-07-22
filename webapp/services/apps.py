import models.documents
from .base import BaseService
from application_context import AppContext
from repositories.apps import AppRepository


class AppService(BaseService):
    def __init__(self, app_repository: AppRepository, app_context: AppContext,config:dict):
        BaseService.__init__(self)
        self.app_repository = app_repository
        self.app_context = app_context
        self.config = config

    async def get_all(self,app_name):

        if self.app_context.app_name != "admin":
            return None
        apps = await self.app_repository.get_all(app_name)
        return apps

    async def get_app_by_name(self, app_name: str,app_name_to_get) -> models.documents.sys_applications:
        if app_name=='admin' and app_name_to_get=='admin':
            ret= models.documents.sys_applications({})
            ret.Name='admin'
            ret.NameLower='admin'
            host = self.config.get('host')
            ret.ReturnUrlAfterSignIn=f"{host.get('schema')}://{host.get('domain')}/login"
            return ret

        app: models.documents.Apps = await self.app_repository.get_app_by_name(app_name, app_name_to_get.lower())
        return app

    async def update_app(self, app: models.documents.Apps, app_name: str):
        await self.app_repository.update(app)

    async def create(self, app:models.documents.Apps)->models.documents.sys_applications:
        return await self.app_repository.create(app)
