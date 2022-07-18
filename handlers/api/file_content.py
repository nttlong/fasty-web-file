from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from webapp.services.files import FileService
from webapp.containers import Container
from webapp.services.file_storage import FileStorageService


@inject
async def get_content(
        app_name: str,
        directory:str,
        file_storage_service: FileStorageService = Depends (Provide[Container.file_storage_service])
):
    file_stm = await file_storage_service.get_file_stream(directory)
    return dict(
        upload_id=directory
    )

