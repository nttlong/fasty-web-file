"""Services module."""
import mimetypes
import os
import pathlib
import uuid
from datetime import datetime

import humanize

import models.documents
from repositories.files import FileRepository
from .base import BaseService


class FileService(BaseService):
    def __init__(self, file_repository: FileRepository) -> None:
        BaseService.__init__(self)
        self.file_repository: FileRepository = file_repository

    async def get_all(self,app_name:str, page_size: int, page_index: int, field_search: str, value_search: str):
        return await self.file_repository.get_all(app_name,page_size, page_index, field_search, value_search)

    async def get_upload_by_id(self,aapp_name:str, upload_id: str):
        return await self.file_repository.get_upload_by_id(upload_id)

    async def add_new_register_upload(self, app_name, register:models.documents.DocUploadRegister)->models.documents.DocUploadRegister:
        server_file_name_only = str(uuid.uuid4())
        register._id = server_file_name_only
        register.RegisterOn = datetime.utcnow()
        register.RegisterOnSeconds = register.RegisterOn.second
        register.RegisterOnMinutes = register.RegisterOn.minute
        register.ChunkSizeInBytes = register.ChunkSizeInKB * 1024
        register.RegisteredBy = app_name
        register.FileExt = os.path.splitext(register.FileName)[1][1:]
        register.FileNameLower = register.FileName.lower()
        register.FileNameOnly = pathlib.Path(register.FileName).stem
        register.FullFileNameWithoutExtenstion = register.FileNameOnly
        register.FullFileNameWithoutExtenstionLower = register.FullFileNameWithoutExtenstion.lower()
        register.FullFileNameLower = register.FileName.lower()
        register.HasThumb = False
        register.MimeType, _ = mimetypes.guess_type(register.FileName)

        register.ServerFileName = f"{server_file_name_only}.{register.FileExt}"
        n, v = divmod(register.SizeInBytes, register.ChunkSizeInBytes)
        if v > 0:
            n += 1
        register.NumOfChunks = n
        register.NumOfChunksCompleted = 0
        register.SizeInHumanReadable = humanize.filesize.naturalsize(register.SizeInBytes)
        await self.file_repository.add_new_register_upload(app_name,register)
        return register
