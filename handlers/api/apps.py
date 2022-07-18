
from fastapi import Depends, Body
from dependency_injector.wiring import inject, Provide

import models.documents
from models.ModelApps import sys_applications
from ..client_model.app import RequestAppInfo
from webapp.containers import Container
from webapp.services.apps import AppService
from utils import OAuth2Redirect



@inject
async def app_get_list(
        app_name: str,
        app_service: AppService = Depends(Provide[Container.apps_services]),
        auth=Depends(OAuth2Redirect())
):
    ret= await app_service.get_all(app_name)
    return ret


@inject
async def app_get(
        app_name: str,
        app_name_get:str,
        app_service: AppService = Depends(Provide[Container.apps_services]),
        auth=Depends(OAuth2Redirect())
):
    ret = await app_service.get_app_by_name(app_name,app_name_get)
    if ret is None:
        return {}
    return ret.DICT
@inject
async def app_update(
        app_name: str,
        app_edit: str,
        Data: RequestAppInfo = Body(embed=True),
        app_service: AppService = Depends(Provide[Container.apps_services]),
        auth=Depends(OAuth2Redirect())
):

    app = sys_applications(
        models.documents.Apps.Name== Data.Name,
        models.documents.Apps.NameLower==Data.Name.lower(),
        models.documents.Apps.Description== Data.Description,

    )
    ret = await app_service.update_app(app,app_edit)
    if ret is None:
        return {}
    return ret.DICT