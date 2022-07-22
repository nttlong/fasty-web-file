


class FileStorageBaseRepository:
   async def get_file_stream(self,app_name, rel_path_to_file):
       """
       Lấy stream của file
       :param app_name:
       :param rel_path_to_file:
       :return:
       """
       raise NotImplemented

   async def add_binary(self,app_name:str, relative_path:str,data: bytes,file_size_in_bytes:int)->(int,int):
       """
       Thêm nội dung vào file
       :param app_name:
       :param relative_path:
       :param data:
       :return (Kích thước sau khi thêm, lần thêm):
       """
       raise NotImplemented

   async def get_len_of_file_stream(self, fsg):
       raise NotImplemented

   async def open_stream(self, file_obj):
       raise NotImplemented

   async def read(self, file_obj, read_size):
       raise NotImplemented

   async def close(self, fsg):
       raise NotImplemented

   async def create_buffer_bytes(self, file_stream, start: int, end: int, chunk_size: int = 1024):
       raise NotImplemented