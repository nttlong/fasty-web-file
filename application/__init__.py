"""Application module."""
import os.path
import pathlib

from fastapi import FastAPI,Request, Response

from webapp.containers import Container
import endpoints
from dependency_injector.wiring import inject
from fastapi.staticfiles import StaticFiles
from utils import OAuth2AndGetUserInfo
from utils import get_token_url

# from .middle_wares.mime_types_javascript_module import add_process_javascript_module
import app_logs

bind_ip=None
bind_port= None
working_dir =str(pathlib.Path(__file__).parent.parent)
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as ex:
        app_logs.debug(ex)
        # you probably want some kind of logging here
        return Response("Server error", status_code=500)


@inject
def create_app() -> FastAPI:
    from .install_mime_types import install_mime_types
    install_mime_types()
    container = Container()
    container.init_resources()
    print('webapp.application.components.JWT')
    container.wire(modules=[

        __name__,"__main__"
    ])
    config = container.config
    global bind_ip
    global bind_port
    bind_ip =config.get('host').get('bind')
    bind_port =config.get('host').get('port')

    db = container.db()

    app = FastAPI()
    app.middleware('http')(catch_exceptions_middleware)
    # app.middleware(config.get('host').get('schema'))(add_process_javascript_module)

    app.container = container
    static_dir = config.get('front-end').get('static')
    if static_dir[0:2]=='./':
        static_dir = static_dir[2:]
        static_dir = os.path.join(working_dir,static_dir).replace('/',os.sep)
    if not os.path.isdir(static_dir):
        raise Exception(f"'{static_dir}' was not found")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    app.include_router(endpoints.router)



    return app

app=None

try:
    app = create_app()
except Exception as e:
    print("start app is error")
    app_logs.debug(e)


