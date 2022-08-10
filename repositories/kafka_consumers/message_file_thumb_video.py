import os
import pathlib
from kafka import KafkaProducer

import app_logs
import broker_group_const
from repositories.file_storage_base import FileStorageBaseRepository
from repositories.kafka_consumers.base import BaseConsumer, FileProcessMessage
from apps_containers.media_content import MediaContainer
from dependency_injector.wiring import inject, Provide

from services.files import FileService
from services.images import ImageFileService
from services.videos import VideoFileService


class ConsumerFileVideoProcessThumb(BaseConsumer):
    def __init__(
            self,
            config,
            file_storage_repo:FileStorageBaseRepository,
            file_service:FileService
    ):
        BaseConsumer.__init__(
            self,
            config,
            broker_group_const.MSG_GROUP_FILE_VIDEO_CREATE_THUMBS)
        self.producer = KafkaProducer(bootstrap_servers=self.brokers)
        self.file_storage_repo=file_storage_repo
        self.file_service=file_service

    @inject
    async def run(self,
                  video_service:VideoFileService=Provide[MediaContainer.video_file_service],
                  image_service:ImageFileService=Provide[MediaContainer.image_file_service]):
        try:

            for msg in self.consumer:
                msg_info = self.convert_msg_to(msg, FileProcessMessage)
                app_logs.info(f"Receive new message "
                              f"App: {msg_info.app_name}"
                              f"UploadId: {msg_info.upload_id}"
                              f"Relative Content: {msg_info.relative_file_path}"
                              f"Message Type: {msg_info.message_type}")
                full_path_to_file =self.get_full_path_from_share_storage(msg_info.app_name, msg_info.relative_file_path)
                register = await self.file_service.get_upload_by_id(
                    app_name= msg_info.app_name,
                    upload_id= msg_info.upload_id
                )
                success, video_file_location = video_service.extract_frame_to_image(full_path_to_file)
                if not success:
                    print(f"Can not get image from video {full_path_to_file}")
                    app_logs.info(f"Can not get image from video {full_path_to_file}")
                thumb_location = image_service.create_thumb(video_file_location, thumb_width=600,
                                                            thumb_height=600)
                file_name = pathlib.Path(full_path_to_file).name.split('.')[0]
                rel_thumb_path = f"{msg_info.upload_id}/thumb/{file_name}.webp".lower()
                with open(thumb_location, "rb") as f:
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
            app_logs.error(e)





