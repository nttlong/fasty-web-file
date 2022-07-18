from dependency_injector import providers,containers
from dependency_injector.containers import DeclarativeContainer
from fastapi import FastAPI
import uvicorn

import web_hosting.models.single_page_application
import web_hosting.models.statics
from web_hosting.web import Web

from fasty_containers.core import ContainerCore




class ContainerApp(DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[
        "web_hosting.templates.single_page_apps"
    ])
    config = providers.Configuration(yaml_files=["config.yml"])
    config.load()
    core = providers.Container(
        ContainerCore,
        config=config.core,
    )
    web_app:Web = providers.Singleton(
        Web,
        config =config
    )
    host_model_static:web_hosting.models.statics.HostModel_Static = providers.Singleton(
        web_hosting.models.statics.HostModel_Static,
        config=config
    )
    host_model_spa: web_hosting.models.single_page_application.HostModel_SPA = providers.Singleton(
        web_hosting.models.single_page_application.HostModel_SPA,
        config =config
    )

