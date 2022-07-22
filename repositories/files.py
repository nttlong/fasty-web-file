"""Repositories module."""
import models.documents
from application_context import AppContext
from .base import BaseRepository
from models import documents as docs
import re


class FileRepository(BaseRepository):

    def __init__(self, session_factory,app_context:AppContext) -> None:
        BaseRepository.__init__(self, session_factory,app_context)
        self.session_factory = session_factory

    async def get_all(self,db_name:str, page_size, page_index, field_search, value_search):
        agg = self.db_context(db_name).aggregate(docs.Files)
        agg.project(
            # docs.Files._id,
            docs.Files.FileName,
            docs.Files.FullFileName,
            docs.Files.HasThumb,
            docs.Files.ServerFileName,
            docs.Files.SizeInHumanReadable,
            docs.Files.Status,
            docs.Files.MimeType,
            docs.Files.IsPublic,
            docs.Files.HasThumb,
            docs.Files.OCRFileId,
            docs.Files.PdfFileId,
            docs.Files.FileNameOnly,
            docs.Files.FileExt,
            FileSize=docs.Files.SizeInBytes,
            ModifiedOn=docs.Files.LastModifiedOn,
            UploadId=docs.Files._id,
            CreatedOn=docs.Files.RegisterOn,
            Media=dict(
                Height=docs.Files.VideoResolutionHeight,
                Width=docs.Files.VideoResolutionWidth,
                Duration=docs.Files.VideoDuration,
                FPS=docs.Files.VideoFPS
            )

        )
        if value_search and value_search != "":
            agg.match(
                docs.Files.FileName == re.compile(value_search)
            )
        agg = agg.pager(page_index, page_size)
        ret = await agg.to_list_async()
        return ret

    async def get_upload_by_id(self,app_name:str, upload_id)->models.documents.Files:
        db_name = self.app_context.get_db_name(app_name)
        ret = await self.db_context(db_name).find_one_async(
            docs.Files,
            docs.Files._id==upload_id
        )

        return ret

    async def add_new_register_upload(self, app_name, register:models.documents.DocUploadRegister):
        db_name = self.app_context.get_db_name(app_name)
        ret= await self.db_context(db_name).insert_one_async(
            models.documents.Files,
            register.DICT
        )

    async def update_register(self, app_name:str, register:models.documents.Files):
        db_name = self.app_context.get_db_name(app_name)
        await self.db_context(db_name).update_one_async(
            models.documents.Files,
            models.documents.Files._id == register._id,
            register.DICT
        )

