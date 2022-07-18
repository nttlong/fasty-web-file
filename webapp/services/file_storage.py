from .base import BaseService
from repositories.file_storage_base import FileStorageBaseRepository


class FileStorageService(BaseService):
    def __init__(self,file_storage_repository):
        self.file_storage_repository:FileStorageBaseRepository = file_storage_repository

    async def get_file_stream(self, directory):
        return await self.file_storage_repository.get_file_stream(directory)