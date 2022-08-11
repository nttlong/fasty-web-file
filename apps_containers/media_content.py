"""Containers module."""
import os.path
import pathlib

from dependency_injector import containers, providers

from services.images import ImageFileService
from services.offices import OfficeFileService
from services.videos import VideoFileService
from start_config import get_config_path

class MediaContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[

        "__main__"

    ])
    config = providers.Configuration(yaml_files=[get_config_path()])
    image_file_service: ImageFileService= providers.Factory(
        ImageFileService,
        config =config
    )

    video_file_service: VideoFileService = providers.Factory(
        VideoFileService,
        config=config
    )

    office_file_service: OfficeFileService = providers.Factory(
        OfficeFileService,
        config =config
    )
