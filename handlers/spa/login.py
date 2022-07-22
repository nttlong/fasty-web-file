from fastapi import Request, Depends
from dependency_injector.wiring import Provide, Provider, inject

from webapp.containers import Container
from fastapi.templating import Jinja2Templates


@inject
async def page_login(
        request: Request,
        templates: Jinja2Templates = Depends(Provide[Container.templates]),
        config: dict = Depends(Provide[Container.config])

):
    app_data = dict(
        full_url_app='',
        full_url_root='/',
        api_url=config.get('front-end').get('api-url')
    )
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "app": app_data
        }
    )
