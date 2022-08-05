import pathlib
from kafka import KafkaProducer

import broker_group_const
from repositories.file_storage_base import FileStorageBaseRepository
from repositories.kafka_consumers.base import BaseConsumer, FileProcessMessage
from apps_containers.media_content import MediaContainer
from dependency_injector.wiring import inject, Provide

from services.files import FileService
from services.images import ImageFileService


class ConsumerFileImageProcessThumb(BaseConsumer):
    def __init__(
            self,
            config,
            logger,
            file_storage_repo:FileStorageBaseRepository,
            file_service:FileService
    ):
        BaseConsumer.__init__(
            self,
            config,
            broker_group_const.MSG_GROUP_FILE_IMAGE_CREATE_THUMBS,logger)
        self.producer = KafkaProducer(bootstrap_servers=self.brokers)
        self.file_storage_repo=file_storage_repo
        self.file_service=file_service

    @inject
    async def run(self,image_service:ImageFileService= Provide[MediaContainer.image_file_service]):
        try:

            for msg in self.consumer:
                msg_info = self.convert_msg_to(msg, FileProcessMessage)
                register = await self.file_service.get_upload_by_id(
                    app_name= msg_info.app_name,
                    upload_id= msg_info.upload_id
                )
                if register is None:
                    continue
                file_name = pathlib.Path(msg_info.content_location).name.split('.')[0]
                rel_thumb_path = f"{msg_info.upload_id}/thumb/{file_name}.webp".lower()
                if await self.file_storage_repo.is_exists(app_name=msg_info.app_name, rel_path_to_file=rel_thumb_path):
                    if register and register.HasThumb==False:
                        register.HasThumb = True
                        await self.file_service.update_register(msg_info.app_name, register)
                    continue
                if register.HasThumb:
                    continue

                if msg_info.content_location:
                    thumb_location= image_service.create_thumb(msg_info.content_location,thumb_width=120,thumb_height=120)

                    with open(thumb_location,"rb") as f:
                        data = f.read()
                        await self.file_storage_repo.add_binary(
                            app_name=msg_info.app_name,
                            relative_path=rel_thumb_path,
                            data=data,
                            file_size_in_bytes=data.__len__()
                        )
                    if register.HasThumb == False:
                        register.HasThumb = True
                        await self.file_service.update_register(msg_info.app_name, register)

        except Exception as e:
            self.logger.error(e)



