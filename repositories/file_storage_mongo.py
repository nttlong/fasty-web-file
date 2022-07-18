import bson
from gridfs import GridFS
from pymongo import MongoClient

from must_implement import MustImplement
from .file_storage_base import FileStorageBaseRepository
from application_context import AppContext
import os

@MustImplement()
class FileStorageMongoDbRepository(FileStorageBaseRepository):

    def __init__(self, db,app_context:AppContext) -> None:
        self.connection:MongoClient =db.connection.delegate
        self.app_context = app_context

    async def get_file_stream(self,rel_path_to_file):
        """
                get stream of file content
                :param rel_path_to_file: relative path to file (root directory get by call get_root_directory
                :return:
                """
        str_mongoddb_file_id = os.path.splitext(rel_path_to_file.split('/')[-1])[0]
        app_name = rel_path_to_file.split('/')[0]
        db_name = self.app_context.get_db_name()
        if db_name is None:
            return None
        mongoddb_file_id = bson.objectid.ObjectId(str_mongoddb_file_id)
        db = self.client.get_database(db_name)
        fs = GridFS(db)
        ret = fs.get(mongoddb_file_id)
        return ret

