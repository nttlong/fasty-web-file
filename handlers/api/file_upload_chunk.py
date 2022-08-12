# import ReCompact_Kafka.producer
import humanize
from fastapi import File, Form, Depends
from typing import Union
import threading
from dependency_injector.wiring import inject, Provide

import app_logs
import services.message_data_types as msg_dataTypes

__lock__ = threading.Lock()

import services.message
from ReCompact import field
from webapp.containers import Container
from handlers.client_model.upload import UploadFilesChunkInfoResult, UploadChunkResult
from utils import OAuth2AndGetUserInfo
from services.file_storage import FileStorageService
from services.files import FileService

"""
Lock dành cach meta, tránh gọi về Database nhiều lần
"""
__meta_upload_cache__ = {}
"""
Cache meta upload. Trong quá trình upload hệ thống sẽ tham khảo đến database của mongodb để xác định quá trình upload
Ví dụ: Hệ thống sẽ cần phải xác định xem nội dung upload đã đạt được bao nhiêu phần trăm.
Để xác định được thông tin này hệ thống sẽ dựa vào Id upload và tìm trong Database Record ứng với Id Upload
và tham khảo đến thông tin phần trăm upload. Quá trình upload 1 file dung lượng lớn mất nhiều thời gian và việc tham khảo đến Database sẽ xảy ra rất nhiều lần.
Để tránh việc tham khảo đến Database nhiều lần cần phải có cơ chế Cache thông tin upload.
Biến này sẽ phụ trách việc cache
"""
@inject
async def files_upload(app_name: str,
                       FilePart: bytes = File(...),
                       UploadId: Union[str, None] = Form(...),
                       Index: Union[int, None] = Form(...),
                       auth=Depends(OAuth2AndGetUserInfo()),
                       file_storage_service: FileStorageService = Depends(Provide[Container.file_storage_service]),
                       file_service: FileService = Depends(Provide[Container.file_service]),
                       message_service: services.message.MessageServices = Depends(Provide[Container.message_service])
                       ):
    """
    Api nay dung de upload noi dung file
    """
    topic_key = "files.services.upload"
    """
    topic báo hiệu 1 file đã được upload 
    """
    app_logs.info("Upload file")
    try:
        register = await file_service.get_upload_by_id(app_name, upload_id=UploadId)

        info = await file_storage_service.add_binary(
            app_name=app_name,
            relative_path=register.FullFileName,
            data=FilePart,
            file_size_in_bytes=register.SizeInBytes

        )
        ret = UploadFilesChunkInfoResult()
        ret.Data = UploadChunkResult()
        ret.Data.SizeInHumanReadable = register.SizeInHumanReadable
        ret.Data.NumOfChunksCompleted = info.uploaded_chunk_index
        ret.Data.SizeUploadedInHumanReadable = humanize.filesize.naturalsize(info.size_in_bytes)
        ret.Data.Percent = (info.size_in_bytes / register.SizeInBytes) * 100
        register.NumOfChunksCompleted = info.uploaded_chunk_index
        message_service.append_binary_content_to_temp(app_name, register.FullFileName, FilePart)
        if info.uploaded_chunk_index + 1 == register.NumOfChunks:
            """
            Complete yet
            """
            register.Status = 1

            from must_implement import new_instance
            uploaded_file = new_instance(msg_dataTypes.UploadedFile,dict(
                relative_file_path = register.FullFileName,
                content_location = message_service.get_content_location(app_name,register.FullFileName),
                app_name = app_name,
                upload_id = register._id

            ))


            print(f"upload with {register._id} send mssage to broker")
            app_logs.debug(f"upload with {register._id} send mssage to broker")
            try:
                message_service.send_message_upload_file_to_brokers(uploaded_file)
            except Exception as e:
                print("Loi")

                app_logs.debug(e)
        await file_service.update_register(app_name, register)
        print("file_service.update_register")
        return ret
    except Exception as e:
        app_logs.debug(e)
        raise e
