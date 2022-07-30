from .base import BaseService
from repositories.file_storage_base import FileStorageBaseRepository

class FileStorageInfo:
    def __init__(self):
        self.size_in_bytes=0
        self.uploaded_chunk_index = 0
        """
        Current chunk index has been uploaded successfully
        """

class FileStorageService(BaseService):
    def __init__(self,file_storage_repository):
        self.file_storage_repository:FileStorageBaseRepository = file_storage_repository

    def get_file_stream(self,app_name, directory):
        return self.file_storage_repository.get_file_stream(app_name,directory)

    async def add_binary(self,
                         app_name:str,
                         relative_path:str,
                         data: bytes,
                         file_size_in_bytes:int)-> FileStorageInfo:
        size, num_of_chunks = await self.file_storage_repository.add_binary(
            app_name,
            relative_path,
            data,
            file_size_in_bytes=file_size_in_bytes
        )
        ret =FileStorageInfo()
        ret.size_in_bytes =size
        ret.uploaded_chunk_index =num_of_chunks
        return ret