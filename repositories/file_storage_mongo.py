import mimetypes
import pathlib
import threading

import bson
import motor.motor_asyncio
import pymongo
from gridfs import GridFS
from pymongo import MongoClient

import ReCompact.db_async
import models.documents
from must_implement import MustImplement
from .file_storage_base import FileStorageBaseRepository
from application_context import AppContext
import os
import ReCompact
from ReCompact import db_async


@ReCompact.document(
    name='fs.files',
    keys=['relative_path']
)
class MongogFileFs:
    _id = (bson.objectid.ObjectId)
    chunkSize = (int)
    length = (int)
    filename = (str)
    relative_path = (str)


mongod_db_file_docs = MongogFileFs()

__mongo_connection__: motor.motor_asyncio.AsyncIOMotorClient=None
__lock__ = threading.Lock()
@MustImplement()
class FileStorageMongoDbRepository(FileStorageBaseRepository):

    def __init__(self,app_context: AppContext,config:dict) -> None:
        """

        :param app_context:
        :param config:
        """
        global __mongo_connection__
        global __lock__
        self.db_config= config.get('storage').get('mongodb')
        self.host = self.db_config.get('host')
        self.port = self.db_config.get('port')
        self.username= self.db_config.get('username')
        self.password= self.db_config.get('password')
        self.authSource= self.db_config.get('authSource')
        self.replicaSet= self.db_config.get('replicaSet')
        self.authMechanism = self.db_config.get('authMechanism')
        if __mongo_connection__ is None:
            __lock__.acquire()
            try:
                if self.replicaSet is not None:
                    __mongo_connection__ = motor.motor_asyncio.AsyncIOMotorClient(

                        host=self.host,
                        port=self.port,
                        username=self.username,
                        password=self.password,
                        authSource=self.authSource,
                        replicaSet=self.replicaSet,
                        authMechanism=self.authMechanism

                    )
                    db = __mongo_connection__.get_database(self.authSource).delegate
                    version_text = db.command({'buildInfo': 1})['version']
                    print(f"connect to mongodb {version_text} ok")
                else:
                    __mongo_connection__ = motor.motor_asyncio.AsyncIOMotorClient(

                        host=self.host,
                        port=self.port,
                        username=self.username,
                        password=self.password,
                        authSource=self.authSource,

                        authMechanism=self.authMechanism

                    )
                db = __mongo_connection__.get_database(self.authSource).delegate

                version_text = db.command({'buildInfo': 1})['version']
                print(f"connect to mongodb {version_text} ok")
            finally:
                __lock__.release()

        self.connection= __mongo_connection__




        self.app_context = app_context
        self.config =config


    async def open_stream(self, file_obj):
        if file_obj.closed:
            fs = GridFS(file_obj._GridOut__files.database)
            file_obj =fs.get(file_obj._id)
            return file_obj
        return file_obj

    async def get_len_of_file_stream(self, fsg):
        return fsg.length
    async def read(self, file_obj, read_size):
        ret =  file_obj.read(read_size)

        return ret
    async def close(self, fsg):
        fsg.close()



    async def get_file_stream(self, app_name: str, rel_path_to_file):
        """
                get stream of file content
                :param app_name:
                :param rel_path_to_file: relative path to file (root directory get by call get_root_directory
                :return:
                """
        db_name = self.app_context.get_db_name(app_name)
        if db_name is None:
            return None
        db = self.connection.get_database(db_name)
        fx =await db.get_collection("fs.files").find_one(dict(relative_path=rel_path_to_file.lower()))
        if fx is None:
            return None
        fs = motor.motor_asyncio.AsyncIOMotorGridFSBucket(db,chunk_size_bytes= 1024)
        # fs = GridFS(db)
        ret = await fs.open_download_stream(fx['_id'])
            # fs.find_one(dict(relative_path=rel_path_to_file.lower()))
        if ret is None:
            return None
        await self.close(ret)
        # ret = fs.get(bson.objectid.ObjectId(file_dict["_id"]))
        return ret

    async def add_binary(self, app_name: str, relative_path: str, data: bytes,file_size_in_bytes:int):
        """
                Thêm nội dung vào file, nếu file chưa có tạo mới.
                Create or append data to file and return unique id of file
                With unique id of file we can get full content of file
                :param server_file_name_only: the name of file at server without extension
                :param rel_path_to_directory: relative path to directory from get_root_directory
                :param filename: filename only including extension
                :param data:
                :return:unique id
                """
        upload_len=0
        db_name = self.app_context.get_db_name(app_name)
        if db_name is None:
            return None
        db = self.connection.get_database(db_name)
        file_dict = await db_async.find_one_async(
            db,
            mongod_db_file_docs,
            mongod_db_file_docs.relative_path == relative_path.lower()

        )
        file_name = pathlib.Path(relative_path).name.lower()
        content_type,_ =mimetypes.guess_type(relative_path)
        if file_dict is None:

            gfs= GridFS(db.delegate)
            fs = gfs.new_file()
            fs.name = file_name
            fs.filename = file_name
            fs.close()

            db.delegate.get_collection("fs.files").update_one(
                {
                  "_id":fs._id
                },
                { "$set": {

                    "chunkSize": data.__len__(),
                    "length": file_size_in_bytes,
                    "filename": file_name,
                    "relative_path": relative_path.lower(),
                    "contentType":content_type,
                    "upload_len":upload_len
                }}
            )

            file = MongogFileFs(
                dict(
                    _id=fs._id,
                    chunkSize=data.__len__(),
                    filename=file_name,
                    length=data.__len__(),
                    relative_path=relative_path.lower(),
                    upload_len=0
                )
            )
        else:
            file = MongogFileFs(file_dict)
            upload_len = file_dict['upload_len']
            upload_len = upload_len + data.__len__()
            db.delegate.get_collection("fs.files").update_one(
                {
                    "_id": file._id
                },
                {"$set": {
                    "upload_len":upload_len
                }}
            )

        chunk_index, m = divmod(upload_len, file.chunkSize)
        if m > 0:
            chunk_index += 1
        fs_chunks = db.get_collection("fs.chunks")
        await fs_chunks.insert_one({
            "_id": bson.objectid.ObjectId(),
            "files_id": file._id,
            "n": chunk_index,
            "data": data
        })
        return upload_len, chunk_index
    async def create_buffer_bytes(self,file_stream,start:int,end:int,chunk_size: int = 1024):
        file_stream = await self.open_stream(file_stream)
        file_stream.seek(start)
        data = [1]
        pos = file_stream.tell()
        while len(data) > 0:
            read_size = min(chunk_size, end + 1 - pos)
            data = await self.read(file_stream, read_size)
            # data= file_obj.read(read_size)
            yield data
        await self.close(file_stream)

    async def is_exists(self, app_name, rel_path_to_file) ->bool:
        db_name = self.app_context.get_db_name(app_name)
        if db_name is None:
            return None
        db = self.connection.get_database(db_name)
        file_dict = await db_async.find_one_async(
            db,
            mongod_db_file_docs,
            mongod_db_file_docs.relative_path == rel_path_to_file.lower()

        )
        return file_dict is not None

