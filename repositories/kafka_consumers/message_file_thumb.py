import mimetypes
import time

from kafka import KafkaProducer

import broker_group_const
import media_containers.containers
from repositories.kafka_consumers.base import BaseConsumer, FileProcessMessage
from media_containers.containers import MediaContainer
from dependency_injector.wiring import inject, Provide

from services.images import ImageFileService
from services.logger_services import LoggerService

class ConsumerFileImageProcessThumb(BaseConsumer):
    def __init__(self, config,logger):
        BaseConsumer.__init__(
            self,
            config,
            broker_group_const.MSG_GROUP_FILE_IMAGE_CREATE_THUMBS,logger)
        self.producer = KafkaProducer(bootstrap_servers=self.brokers)

    @inject
    def run(self,image_service:ImageFileService= Provide[MediaContainer.image_file_service]):
        try:
            time.sleep(1)
            for msg in self.consumer:

                msg_info = self.convert_msg_to(msg, FileProcessMessage)
                image_service.create_thumb()
                
        except Exception as e:
            self.logger.error(e)



