import time

import media_containers.containers
from brokers_services import register_processing
from dependency_injector.wiring import Provide, inject
from brokers_services.containers import FileProcessingContainer
from repositories.kafka_consumers.files_uploaded import ConsumerFileUploaded
from repositories.kafka_consumers.message_file_thumb import ConsumerFileImageProcessThumb
from media_containers.containers import MediaContainer

@inject
def run(consumer_file_image_process_thumb: ConsumerFileImageProcessThumb = Provide[FileProcessingContainer.consumer_file_image_process_thumb]):
    consumer_file_image_process_thumb.start()




register_processing(run,other_container=[media_containers.containers.MediaContainer])()


