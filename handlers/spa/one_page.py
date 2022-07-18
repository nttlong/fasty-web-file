from fastapi import Request, Depends, Response
from dependency_injector.wiring import Provide, Provider,inject
from webapp.containers import Container
from fastapi.templating import Jinja2Templates
import os



@inject
async def page_only_one(directory: str, request: Request,
                        templates: Jinja2Templates= Depends(Provide[Container.templates]),
                        config: dict = Depends(Provider[Container.config])):
    directory = directory.split('?')[0]
    check_dir_path = os.path.join(config.get('front-end').get('static'), "views", directory.replace('/', os.sep))
    if not os.path.exists(check_dir_path):
        return Response(status_code=401)
    app_data = dict(
        full_url_app='',
        full_url_root='/',
        api_url=config.get('front-end').get('api-url')
    )
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app": app_data
        }
    )