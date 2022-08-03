import time

from brokers_services import register_processing
from dependency_injector.wiring import Provide, inject
from brokers_services.containers import FileProcessingContainer
from repositories.kafka_consumers.files_uploaded import ConsumerFileUploaded
from repositories.kafka_consumers.base import FileProcessMessage


@inject
def run(consumer_file_uploaded: ConsumerFileUploaded = Provide[FileProcessingContainer.consumer_file_uploaded]):
    consumer_file_uploaded.start()




register_processing(run)()


