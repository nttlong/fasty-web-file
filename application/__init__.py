"""Application module."""
import os.path

from fastapi import FastAPI

from webapp.containers import Container
import endpoints
from dependency_injector.wiring import inject
from fastapi.staticfiles import StaticFiles
from utils import OAuth2Redirect
from utils import get_token_url
@inject
def create_app() -> FastAPI:
    container = Container()
    container.init_resources()
    print('webapp.application.components.JWT')
    container.wire(modules=[
        'webapp.application',
        __name__,"__main__"
    ])
    config = container.config

    db = container.db()

    app = FastAPI()
    app.container = container
    static_dir = config.get('front-end').get('static')
    if not os.path.isdir(static_dir):
        raise Exception(f"'{static_dir}' was not found")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    app.include_router(endpoints.router)



    return app


app = create_app()
