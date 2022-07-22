import uvicorn
from fastapi import FastAPI
from .base import Base
import sys
class Web(Base):
    def __init__(self,config):
        Base.__init__(self,config)
        print("WebApplication __init")
        print(config)
        self.config:dict =config

    def get_app(self)->FastAPI:
        import web_hosting
        return web_hosting.app
    @property
    def start_module_name(self):
        import web_hosting
        return web_hosting.__name__
    def start(self):
        self.app.include_router(self.router)
        uvicorn.run(
            f"{self.start_module_name}:app",
            host=self.config.get('host').get('bind'),
            port=self.config.get('host').get('port'),
            debug=True,
            reload=True
        )