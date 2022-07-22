from starlette.templating import Jinja2Templates
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Request

import web_hosting
from ..base import Base
import os
import web_hosting.templates.single_page_apps
class HostModel_SPA(Base):
    def __init__(self, config):
        app = self.app
        self.templates_dir = config.get('front-end').get('server-templates')
        if not os.path.isdir(self.templates_dir):
            raise Exception(f"{self.templates_dir} was not found")
        self.templates = Jinja2Templates(
            directory=self.templates_dir
        )


