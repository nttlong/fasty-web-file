from starlette.staticfiles import StaticFiles

from ..base import Base
import os
class HostModel_Static(Base):
    def __init__(self,config):
        app =self.app
        self.static_dir = config.get('front-end').get('static')
        if not os.path.isdir(self.static_dir):
            raise Exception(f"'{self.static_dir}' was not found")

    def start(self):
        import web_hosting
        web_hosting.app.mount("/static", StaticFiles(directory=self.static_dir), name="static")