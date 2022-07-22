from dependency_injector import providers,containers
from dependency_injector.containers import DeclarativeContainer
import logging


class ContainerCore(DeclarativeContainer):

    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )
