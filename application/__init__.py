"""Application module."""
import os.path
import pathlib

from fastapi import FastAPI,Request

from webapp.containers import Container
import endpoints
from dependency_injector.wiring import inject
from fastapi.staticfiles import StaticFiles
from utils import OAuth2AndGetUserInfo
from utils import get_token_url
from .install_mime_types import install_mime_types
from .middle_wares.mime_types_javascript_module import add_process_javascript_module
import app_logs
install_mime_types()
bind_ip=None
bind_port= None
working_dir =str(pathlib.Path(__file__).parent.parent)
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
    global bind_ip
    global bind_port
    bind_ip =config.get('host').get('bind')
    bind_port =config.get('host').get('port')

    db = container.db()

    app = FastAPI()

    app.middleware(config.get('host').get('schema'))(add_process_javascript_module)

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
    app_logs.debug(e)


