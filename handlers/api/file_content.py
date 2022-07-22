import mimetypes

from dependency_injector.wiring import inject, Provide
from fastapi import Depends

import utils.htt_streaming
from webapp.services.files import FileService
from webapp.containers import Container
from webapp.services.file_storage import FileStorageService
from fastapi import Request

@inject
async def get_content(
        app_name: str,
        directory:str,
        request:Request,
        file_storage_service: FileStorageService = Depends (Provide[Container.file_storage_service]),
        file_service:FileService = Depends(Provide[Container.file_service])
):

    thumnb = directory.split('/')[1]
    if thumnb=='thumb':
        upload_id = directory.split('/')[0]
        register = await file_service.get_upload_by_id(app_name, upload_id)
        if register.ThumbFileId is not None:
            db_name = file_service.file_repository.app_context.get_db_name(app_name)
            db = file_service.file_repository.db_context(db_name)
            db.db.delegate.get_collection("fs.files").update_one({
                "_id": register.ThumbFileId,

            },{
                "$set": {"relative_path":directory.lower()}
            })
        print('error')
    # try:
    file_stm = await file_storage_service.get_file_stream(app_name,directory)


    # fix data cu:
    if file_stm is None:
        upload_id = directory.split('/')[0]
        if upload_id=="thumnb":
            return None
        register = await  file_service.get_upload_by_id(app_name,upload_id)
        if register is not None:
            db_name = file_service.file_repository.app_context.get_db_name(app_name)
            db = file_storage_service.file_storage_repository.connection.get_database(db_name)
            if register.MainFileId is not None:
                db.get_collection("fs.files").update_one(
                    {
                        "_id":register.MainFileId

                    },
                    {
                        "$set":{
                            "relative_path":directory.lower()
                        }
                    }
                )

        file_stm = await file_storage_service.get_file_stream(app_name, directory)

    content_type,_= mimetypes.guess_type(directory)
    res = await utils.htt_streaming.streaming(
        file_store_repository=file_storage_service.file_storage_repository,
        fsg= file_stm,
        # file_store_repository=file_storage_service.file_storage_repository,
        request= request,
        content_type= content_type

    )

    return res
    # except Exception as e:
    #     print(e)

