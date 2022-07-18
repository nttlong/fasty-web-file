from fastapi import Request, Depends
from dependency_injector.wiring import Provide,Provider
from ..routers import router
from ...containers import Container
from fastapi.templating import Jinja2Templates
@router.get("/")
async def page_index(
        request: Request

        ):
    templates:Jinja2Templates = Provide[Container.templates].provider
    config:dict = Provider[Container.config].provider
    app_data =dict(
        full_url_app='',
        full_url_root='/',
        api_url=config.get('front-end').get('api-url')
    )
    return templates.TemplateResponse(
        "index.html",
        {
            "request":request,
            "app": app_data
        }
    )