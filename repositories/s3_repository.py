import mimetypes
import pathlib
import boto3
import humanize.filesize
from boto3.s3.transfer import TransferConfig
from smart_open import open
import bson
from gridfs import GridFS
from pymongo import MongoClient

import ReCompact.db_async
import models.documents
from must_implement import MustImplement
from .file_storage_base import FileStorageBaseRepository
from .s3_stream import S3Stream,open_s3_stream
from application_context import AppContext
import os

__cache__ ={}


def ProgressPercentage(fs):
    print(fs)



def uploadFileS3(access_key_id, secret_access_key,temp_file,bucket_name,s3_file_path):

    s3 = boto3.resource('s3',
                        aws_access_key_id=access_key_id,
                        aws_secret_access_key=secret_access_key)
    bucket = s3.Bucket(name=bucket_name)

    if not bucket.creation_date:
        s3.create_bucket(Bucket=bucket_name)
    chunk_size = 1024*1024*50
    boto_session = boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    )
    with open(
            f's3://{bucket_name}/{s3_file_path}',
            'wb',
            transport_params={'client': boto_session.client('s3')}) as fout:
        data: bytes = [1]
        len =0
        with open(temp_file,"rb") as file:
            data = file.read(chunk_size)
            while data.__len__()>0:
                fout.write(data)
                len+= data.__len__()
                data = file.read(chunk_size)
                print(humanize.filesize.naturalsize(len))


@MustImplement()
class FileStorageS3DbRepository(FileStorageBaseRepository):

    def __init__(self, app_context: AppContext,config:dict) -> None:
        storage_config = config.get('storage')
        self.app_context = app_context
        self.config =storage_config
        self.access_key_id=storage_config.get('s3').get('access-key-id')
        self.secret_access_key = storage_config.get('s3').get('secret-access-key')
        self.tem_directory = storage_config.get('s3').get('tmp-directory')


    async def open_stream(self, file_obj:S3Stream):
        return file_obj

    async def get_len_of_file_stream(self, fsg:S3Stream):
        return fsg.size()
        # pah=r"\\192.168.18.36\Share\s3-tmp\app-test-dev\f807caa7-5d24-4e61-a7d5-79279c3e10f0\4k-quality.mp4"
        # return os.path.getsize(pah)



    async def read(self, file_obj:S3Stream, read_size):
        ret = file_obj.read(read_size)
        return ret
    async def close(self, fsg:S3Stream):
        fsg.close()
    async def get_file_stream(self, app_name: str, rel_path_to_file):
        """
                get stream of file content
                :param app_name:
                :param rel_path_to_file: relative path to file (root directory get by call get_root_directory
                :return:
                """
        # from s3streaming import s3_open
        bucket_name = f"lv-bucket-{app_name}"
        # boto_session = boto3.Session(
        #     aws_access_key_id=self.access_key_id,
        #     aws_secret_access_key=self.secret_access_key
        # )
        # ret = s3_open(f's3://{bucket_name}/{rel_path_to_file.lower()}', boto_session=boto3.session.Session())
        # return ret
        stm = open_s3_stream(self.access_key_id,self.secret_access_key,bucket_name,rel_path_to_file)
        return stm

    # def uploadFileS3(self,filename):
    #     config = TransferConfig(multipart_threshold=1024 * 25, max_concurrency=10,
    #                             multipart_chunksize=1024 * 25, use_threads=True)
    #     file = FILE_PATH + filename
    #     key = KEY_PATH + filename
    #     s3_client.upload_file(file, S3_BUCKET, key,
    #                           ExtraArgs={'ACL': 'public-read', 'ContentType': 'video/mp4'},
    #                           Config=config,
    #                           Callback=ProgressPercentage(file)
    #                           )

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


        global __cache__
        tmp_dir = str(pathlib.Path(os.path.join(self.tem_directory,app_name,relative_path).replace('/',os.sep)).parent)
        if not os.path.isdir(tmp_dir):
            os.makedirs(tmp_dir)
        tmp_file =    os.path.join(self.tem_directory,app_name,relative_path).replace('/',os.sep).lower()
        bucket_name = f"lv-bucket-{app_name}"


        file_len,chunkSize =__cache__.get(f"{bucket_name}/{relative_path}",(0,data.__len__()))
        if not os.path.isfile(tmp_file):
            with open(tmp_file,"wb") as file:
                file.write(data)
        else:
            with open(tmp_file,"ab") as file:
                file.write(data)

        file_len+= data.__len__()
        __cache__[f"{bucket_name}/{relative_path}"]=(file_len,chunkSize)
        chunk_index, m = divmod(file_len, chunkSize)
        if m > 0:
            chunk_index += 1
        if file_size_in_bytes == file_len:
            import threading

            th_run = threading.Thread(target=uploadFileS3, args=(self.access_key_id,self.secret_access_key , tmp_file, bucket_name, relative_path,))
            th_run.start()
            # th_run.join()
        return file_len, chunk_index
    async def create_buffer_bytes(self,file_stream,start:int,end:int,chunk_size: int = 1024*1024*3):
        file_stream = await self.open_stream(file_stream)
        # for x in file_stream:
        #     print(x)
        #     yield x
        file_stream.seek(start)
        chunk_size: int = 1024 * 1024 * 3
        ret = file_stream.read(chunk_size)
        for x in ret:
            yield x

        # return ret
        # data = [1]
        # pos = file_stream.tell()
        # chunk_size: int = 1024 * 1024 * 3
        # while len(data) > 0:
        #     read_size = min(chunk_size, end + 1 - pos)
        #     data = await self.read(file_stream, read_size)
        #     # data= file_obj.read(read_size)
        #     yield data
        # await self.close(file_stream)