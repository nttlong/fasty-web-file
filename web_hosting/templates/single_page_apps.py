from fastapi import Request, Depends
from dependency_injector.wiring import Provide, Provider, inject

from fastapi.templating import Jinja2Templates
import web_hosting.models.single_page_application
from fasty_containers.app import ContainerApp
@web_hosting.app.get('/')
@inject
async def page_index(
        request: Request,
        spa: web_hosting.models.single_page_application.HostModel_SPA = Depends(Provide[ContainerApp.host_model_spa]),
        config: dict = Depends(Provide[ContainerApp.config])

):
    app_data = dict(
        full_url_app='',
        full_url_root='/',
        api_url=config.get('front-end').get('api-url')
    )
    return spa.templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app": app_data
        }
    )

