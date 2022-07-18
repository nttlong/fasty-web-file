"""
API liệt kê danh sách các file
"""

import models.documents
import webapp.containers
from fastapi import Depends, Body
from dependency_injector.wiring import inject, Provide
from handlers.client_model.files_register import RegisterUploadInfoResult, RegisterUploadInfo, RegisterUploadResult
from utils import OAuth2Redirect
from webapp.services.files import FileService

"""
Cấu trúc trả về
"""


@inject
async def register_new_upload(
        app_name: str,
        Data: RegisterUploadInfo = Body(embed=True),
        auth=Depends(OAuth2Redirect()),
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
    ret.Data.ServerFilePath = register.ServerFileName
    ret.Data.UrlOfServerPath = f"{api_url}/{app_name}/file/{register._id}/{register.FileName}"
    ret.Data.RelUrlOfServerPath = f"{app_name}/file/{register._id}/{register.FileName}"

    ret.Data.ServerFilePath = register.FullFileName
    ret.Data.NumOfChunks = register.NumOfChunks
    ret.Data.ChunkSizeInBytes = register.ChunkSizeInBytes
    ret.Data.MimeType = register.MimeType
    ret.Data.FileSize = Data.FileSize
    return ret
    # ret = RegisterUploadInfoResult()
    # for k in list(Data.__dict__.keys()):
    #     if Data.__dict__.get(k, None) is None:
    #         ret.Error = error.Error()
    #         ret.Error.Code = ReCompact.db_async.ErrorType.DATA_REQUIRE.value
    #         ret.Error.Fields = [k]
    #         ret.Error.Message = f"'{k}' is require"
    #         return ret
    # upload_id = str(uuid.uuid4())
    # """
    # Số upload
    # """
    # db_name = await fasty.JWT.get_db_name_async(app_name)
    # if db_name is None:
    #     """
    #     Applcation không tìm thấy
    #     """
    #     return Response(status_code=403)
    #
    # db_context = get_db_context(db_name)
    # _, file_extension = os.path.splitext(Data.FileName)
    # mime_type, _ = mimetypes.guess_type(Data.FileName)
    # reg_now = datetime.datetime.now()
    # chunk_size = Data.ChunkSizeInKB * 1024
    # num_of_chunks, remain = divmod(Data.FileSize, chunk_size)
    # if remain > 0:
    #     num_of_chunks += 1
    # filename_only = Path(Data.FileName).stem
    # ret_upload = await  db_context.insert_one_async(
    #     docs.Files,
    #     docs.Files._id == upload_id,
    #     docs.Files.FileName == Data.FileName,
    #     docs.Files.FileNameLower == Data.FileName.lower(),
    #     docs.Files.FileNameOnly == filename_only,
    #     docs.Files.FileExt == file_extension[1:],
    #     docs.Files.FullFileName == f"{upload_id}/{Data.FileName}",
    #     docs.Files.FullFileNameLower == f"{upload_id}/{Data.FileName.lower()}",
    #     docs.Files.FullFileNameWithoutExtenstion==f"{upload_id}/{filename_only}",
    #     docs.Files.FullFileNameWithoutExtenstionLower== f"{upload_id}/{filename_only}".lower(),
    #     docs.Files.ChunkSizeInKB == Data.ChunkSizeInKB,
    #     docs.Files.ChunkSizeInBytes == Data.ChunkSizeInKB * 1024,
    #     docs.Files.SizeInBytes == Data.FileSize,
    #     docs.Files.NumOfChunks == num_of_chunks,
    #     docs.Files.NumOfChunksCompleted == 0,
    #     docs.Files.SizeInHumanReadable == humanize.filesize.naturalsize(Data.FileSize),
    #     docs.Files.SizeUploaded == 0,
    #     docs.Files.ProcessHistories == [],
    #     docs.Files.ServerFileName==f"{upload_id}.{file_extension}",
    #
    #
    #     docs.Files.MimeType == mime_type,
    #     docs.Files.IsPublic == Data.IsPublic,
    #     docs.Files.Status == 0,
    #     docs.Files.RegisterOn == reg_now,
    #     docs.Files.RegisterOnDays == reg_now.day,
    #     docs.Files.RegisterOnHours == reg_now.hour,
    #     docs.Files.RegisterOnYears == reg_now.year,
    #     docs.Files.RegisterOnSeconds == reg_now.second,
    #     docs.Files.RegisterOnMinutes == reg_now.minute
    #
    # )
    # ret.Data = register_new_upload_input.RegisterUploadResult()
    # ret.Data.SizeInHumanReadable = ret_upload[docs.Files.SizeInHumanReadable.__name__]
    #
    # ret.Data.UrlThumb = f"{fasty.config.app.api_url}/thumb/{ret_upload[docs.Files._id.__name__]}/{ret_upload[docs.Files.FileNameOnly.__name__]}.png"
    # ret.Data.RelUrlThumb = f"thumb/{ret_upload[docs.Files._id.__name__]}/{ret_upload[docs.Files.FileNameOnly.__name__]}.png"
    # ret.Data.ServerFilePath=ret_upload[docs.Files.ServerFileName.__name__]
    # ret.Data.UrlOfServerPath =f"{fasty.config.app.api_url}/{app_name}/file/{upload_id}/{ret_upload['FileName']}"
    # ret.Data.RelUrlOfServerPath = f"{app_name}/file/{upload_id}/{ret_upload['FileName']}"
    # ret.Data.UploadId = ret_upload["_id"]
    # ret.Data.ServerFilePath=ret_upload[docs.Files.FullFileName.__name__]
    # ret.Data.NumOfChunks = num_of_chunks
    # ret.Data.ChunkSizeInBytes = chunk_size
    # ret.Data.MimeType = mime_type
    # ret.Data.FileSize=Data.FileSize
    # return ret
