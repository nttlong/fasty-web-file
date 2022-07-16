"""Application module."""
import datetime

from fastapi import FastAPI,Request

from .containers import Container
from . import endpoints
from .contex import AppContext
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
def create_app() -> FastAPI:
    container = Container()

    db = container.db()


    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)

    @app.middleware("http")

    async def add_process_time_header(request: Request, call_next,app_context: AppContext = Provide[Container.user_service]):
        # app_name= request.scope.get('path_params').get('app_name')
        fx: AppContext = await app_context.async_()
        print(f'current_app={fx.get_db_name()}')
        print(request.path_params)
        print(request.url,request.scope.get('path_params'))
        print(request.scope.get('endpoint'))
        start_time = datetime.datetime.now()
        response = await call_next(request)
        process_time = datetime.datetime.now() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        return response
    return app


app = create_app()
