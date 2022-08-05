# """Containers module."""
import os.path
import pathlib
#
from dependency_injector import containers, providers


class UtilsContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "__main__"
    ])


