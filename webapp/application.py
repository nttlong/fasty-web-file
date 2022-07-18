"""Application module."""
import datetime
import os.path

from fastapi import FastAPI,Request

from .containers import Container
from . import endpoints
from .contex import AppContext
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from fastapi.staticfiles import StaticFiles

def create_app() -> FastAPI:
    container = Container()
    config = container.config


    db = container.db()


    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)

    # @app.middleware("http")
    #
    # async def add_process_time_header(request: Request, call_next,app_context: AppContext = Provide[Container.user_service]):
    #     # app_name= request.scope.get('path_params').get('app_name')
    #
    #     print(f'current_app={fx.get_db_name()}')
    #     print(request.path_params)
    #     print(request.url,request.scope.get('path_params'))
    #     print(request.scope.get('endpoint'))
    #     start_time = datetime.datetime.now()
    #     response = await call_next(request)
    #     process_time = datetime.datetime.now() - start_time
    #     response.headers["X-Process-Time"] = str(process_time)
    #
    #     return response
    static_dir = config.get('front-end').get('static')
    if not os.path.isdir(static_dir):
        raise Exception(f"'{static_dir}' was not found")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


    return app


app = create_app()
