import mimetypes
import time

from kafka import KafkaProducer

import broker_group_const
from repositories.kafka_consumers.base import BaseConsumer, FileProcessMessage
from dependency_injector.wiring import inject, provided

from services.logger_services import LoggerService


class ConsumerFileUploaded(BaseConsumer):
    def __init__(self, config,logger):
        BaseConsumer.__init__(
            self,
            config,
            broker_group_const.MSG_GROUP_FILE_UPLOADED,logger)
        self.producer = KafkaProducer(bootstrap_servers=self.brokers)

    async def run(self):
        try:

            for msg in self.consumer:

                msg_info = self.convert_msg_to(msg, FileProcessMessage)
                mime_type, _ = mimetypes.guess_type(msg_info.content_location)
                print(f"Receive new topic {msg_info.message_type}\n"
                      f"App:{msg_info.app_name}\n"
                      f"Resource location:{msg_info.content_location}\n"
                      f"Media id:{msg_info.upload_id}")

                if 'image/' in mime_type:
                    self.producer.send(
                        broker_group_const.MSG_GROUP_FILE_IMAGE_CREATE_THUMBS,
                        self.convert_object_to_binary(msg_info)
                    )
                    self.logger.error(f"{broker_group_const.MSG_GROUP_FILE_IMAGE_CREATE_THUMBS} was raise\n"
                                      f"{msg_info.content_location}")
                    self.producer.send(
                        broker_group_const.MSG_GROUP_FILE_IMAGE_OCR,
                        self.convert_object_to_binary(msg_info)
                    )
                    self.logger.error(f"{broker_group_const.MSG_GROUP_FILE_IMAGE_CREATE_THUMBS} was raise\n"
                                      f"{msg_info.content_location}")
                elif mime_type=="application/pdf":
                    self.producer.send(
                        broker_group_const.MSG_GROUP_FILE_PDF_CREATE_THUMBS,
                        self.convert_object_to_binary(msg_info)
                    )
                    self.logger.error(f"{broker_group_const.MSG_GROUP_FILE_PDF_CREATE_THUMBS} was raise\n"
                                      f"{msg_info.content_location}")
                    self.producer.send(
                        broker_group_const.MSG_GROUP_FILE_PDF_CREATE_OCR,
                        self.convert_object_to_binary(msg_info)
                    )
                    self.logger.error(f"{broker_group_const.MSG_GROUP_FILE_PDF_CREATE_OCR} was raise\n"
                                      f"{msg_info.content_location}")
                elif 'application/vnd.openxmlformats-officedocument' in mime_type:
                    self.producer.send(
                        broker_group_const.MSG_GROUP_FILE_OFFICE_CREATE_THUMBS,
                        self.convert_object_to_binary(msg_info)
                    )
                    self.logger.error(f"{broker_group_const.MSG_GROUP_FILE_OFFICE_CREATE_THUMBS} was raise\n"
                                      f"{msg_info.content_location}")
                    self.producer.send(
                        broker_group_const.MSG_GROUP_FILE_OFFICE_CREATE_SEARCH_INDEX,
                        self.convert_object_to_binary(msg_info)
                    )
                    self.logger.error(f"{broker_group_const.MSG_GROUP_FILE_OFFICE_CREATE_SEARCH_INDEX} was raise\n"
                                      f"{msg_info.content_location}")
                elif 'video/' in mime_type:
                    self.producer.send(
                        broker_group_const.MSG_GROUP_FILE_VIDEO_CREATE_THUMBS,
                        self.convert_object_to_binary(msg_info)
                    )
                    self.logger.error(f"{broker_group_const.MSG_GROUP_FILE_VIDEO_CREATE_THUMBS} was raise\n"
                                      f"{msg_info.content_location}")

                else:
                    print("OK")
                    self.logger.error("--------------------------------")
                    self.logger.error("not impletement")
                    self.logger.error(self.get_msg_data(msg))
                    self.logger.error("--------------------------------")
        except Exception as e:
            self.logger.error(e)



