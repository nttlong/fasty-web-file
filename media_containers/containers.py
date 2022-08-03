"""Containers module."""
import os.path
import pathlib

from dependency_injector import containers, providers

from services.images import ImageFileService


class MediaContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[

        "__main__"

    ])
    config = providers.Configuration(yaml_files=["config.yml"])
    image_file_service: ImageFileService= providers.Factory(
        ImageFileService,
        config =config
    )




