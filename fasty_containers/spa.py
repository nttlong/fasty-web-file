from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from .core import ContainerCore
from app_services.spa import SPAServices

class ContainerSPA(DeclarativeContainer):
    spa_service = providers.Singleton(
        SPAServices
    )


