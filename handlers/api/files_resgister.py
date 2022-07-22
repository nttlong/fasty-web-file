"""
API liệt kê danh sách các file
"""

import models.documents
import webapp.containers
from fastapi import Depends, Body
from dependency_injector.wiring import inject, Provide
from handlers.client_model.files_register import RegisterUploadInfoResult, RegisterUploadInfo, RegisterUploadResult
from utils import OAuth2AndGetUserInfo
from webapp.services.files import FileService

"""
Cấu trúc trả về
"""


@inject
async def register_new_upload(
        app_name: str,
        Data: RegisterUploadInfo = Body(embed=True),
        auth=Depends(OAuth2AndGetUserInfo()),
        file_service: FileService = Depends(Provide[webapp.containers.Container.file_service]),
        config: dict = Depends(Provide[webapp.containers.Container.config])
):
    """

    :param config:
    :param file_service:
    :param auth:
    :param app_name: Ứng dụng nào cần đăng ký Upload
    :param Data: Thông tin đăng ký Upload
    :param token:
    :return:
    """

    register = models.documents.DocUploadRegister(Data.__dict__)
    register.SizeInBytes = Data.FileSize
    ret = RegisterUploadInfoResult()

    ret_insert = await file_service.add_new_register_upload(
        app_name,
        register
    )
    ret.Data = RegisterUploadResult()
    ret.Data.FileSize = Data.FileSize
    ret.Data.UploadId = register._id
    ret.Data.ChunkSizeInBytes = register.ChunkSizeInBytes
    ret.Data.NumOfChunks = register.NumOfChunks
    ret.Data.SizeInHumanReadable = register.SizeInHumanReadable
    ret.Data.NumOfChunks = register.NumOfChunks
    api_url = config.get('front-end').get('api-url')
    ret.Data.UrlThumb = f"{api_url}/thumb/{register._id}/{register.FileNameOnly}.png"
    ret.Data.RelUrlThumb = f"thumb/{register._id}/{register.FileNameOnly}.png"
    ret.Data.ServerFilePath = register.FullFileName
    ret.Data.UrlOfServerPath = f"{api_url}/{app_name}/file/{register._id}/{register.FileName}"
    ret.Data.RelUrlOfServerPath = f"{app_name}/file/{register._id}/{register.FileName}"


    ret.Data.NumOfChunks = register.NumOfChunks
    ret.Data.ChunkSizeInBytes = register.ChunkSizeInBytes
    ret.Data.MimeType = register.MimeType
    ret.Data.FileSize = Data.FileSize
    return ret
