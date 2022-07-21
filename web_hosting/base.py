from fastapi import FastAPI,APIRouter




class Base:
    def __init__(self,config):
        self.config=config
    @property
    def app(self)->FastAPI:
        import web_hosting
        return web_hosting.app
    @property
    def router(self)->APIRouter:
        import web_hosting
        return web_hosting.router
