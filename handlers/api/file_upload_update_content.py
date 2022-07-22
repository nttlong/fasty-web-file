from  dependency_injector.wiring import inject,Provide
from fastapi import Form, File, Depends

import webapp.containers
from utils import OAuth2AndGetUserInfo
from webapp.services.file_storage import FileStorageService
from webapp.services.files import FileService
from pydantic import BaseModel
from pydantic.fields import Field
from typing import Union
from ..client_model.errors import Error as ret_error,ErrorType
from webapp.containers import Container
class ContentResult(BaseModel):
    pass
class UpdateContentResult(BaseModel):
    Data: Union[ContentResult, None] = Field(description="Kết quả nếu không lỗi")
    Error: Union[ret_error, None] = Field(description="Lỗi")

@inject

async def create_or_repace_thumb(
        app_name: str,
        File: bytes = File(...),
        UploadId: Union[str, None] = Form(...),
        auth=Depends(OAuth2AndGetUserInfo()),
        file_storage_service: FileStorageService = Depends(Provide[Container.file_storage_service]),
        file_service: FileService = Depends(Provide[Container.file_service])
):
    ret= UpdateContentResult()
    register = file_service.get_upload_by_id(UploadId)
    if register is None:
        ret.Error= ret_error()
        ret.Error.Code= ErrorType.DATA_NOT_FOUND.name
        ret.Error.Message ="File not found"
        return ret
    rel_thum_path=f"{UploadId}/thumb/{register._id}"

    file_storage_service.add_binary(app_name,)
    return {}
