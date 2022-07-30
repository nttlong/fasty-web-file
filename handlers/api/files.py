from time import strftime, gmtime

from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from webapp.containers import Container
from application_context import AppContext
from utils import OAuth2AndGetUserInfo
from services.files import FileService
from fastapi import Request
from typing import Union
from models import documents as docs
from pydantic import BaseModel

class Filter(BaseModel):
    """
    Bộ lọc
    """
    PageIndex: int=0
    """
    Bỏ qua
    """
    PageSize: int =50
    FieldSearch: Union[str,None]
    """
    Filed cần tìm
    """
    ValueSearch: Union[str,None]
    class Config:
        schema_extra = {
            "filter": {
                "PageIndex": 0,
                "PageSize":50
            }
        }



@inject
async def get_list(
        app_name: str,
        filter:Filter,
        request:Request,
        file_service: FileService = Depends(Provide[Container.file_service]),
        config:dict =Depends(Provide[Container.config]),
        app_context:AppContext =Depends(Provide[Container.app_context]),
        auth=Depends(OAuth2AndGetUserInfo()),

):
    """
    Lấy danh sách các file
    :param file_service:
    :param app_name:
    :param auth:
    :return:
    """

    lst_of_files = await file_service.get_all(
        app_name,
        page_size= filter.PageSize,
        page_index = filter.PageIndex,
        field_search = filter.FieldSearch,
        value_search = filter.ValueSearch

    )
    url = config.get('front-end').get('api-url')
    for x in lst_of_files:
        full_filename_without_extenstion = x.get(docs.Files.FullFileNameWithoutExtenstion.__name__)
        point_to_file =f"/{app_name}/file/{x['UploadId']}/{x[docs.Files.FileName.__name__]}"
        # x["UrlOfServerPath"] = url + f"/{app_name}/file/{x[docs.Files.FullFileName.__name__]}?{share_key.key}={share_key.value}"
        x["UrlOfServerPath"] = url + point_to_file
        x["AppName"] = app_name
        x["RelUrlOfServerPath"] = point_to_file
        if x.get("HasThumb",False):
            x["ThumbUrl"] = url + f"/{app_name}/file/{x['UploadId']}/thumb/{x[docs.Files.FileName.__name__]}.png"
        if x.get("Media") and x["Media"].get("Duration"):
            x["DurationHumanReadable"] = strftime("%H:%M:%S", gmtime(x["Media"]["Duration"]))
        if x.get(docs.Files.OCRFileId.__name__):
            """
            /{app_name}/file-ocr/{directory:path}
            """
            x[docs.Files.OCRFileId.__name__] = None
            x["OcrContentUrl"] = url + f"/{app_name}/file-ocr/{full_filename_without_extenstion}.pdf"
        if x.get(docs.Files.PdfFileId.__name__):
            x.get(docs.Files.PdfFileId.__name__)
            x["PdfContentUrl"] = url + f"/{app_name}/file-pdf/{full_filename_without_extenstion}.pdf"

    return lst_of_files

