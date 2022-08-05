import sys

import apps_containers.tracking
import exten_services

if "dev" in sys.argv:
    import developer
import time
from start_config import get_config_path

print(get_config_path())
from brokers_services import register_processing
from dependency_injector.wiring import Provide, inject
from brokers_services.containers import FileProcessingContainer
from repositories.kafka_consumers.files_uploaded import ConsumerFileUploaded
from repositories.kafka_consumers.base import FileProcessMessage
from exten_services.tracking import TrackingService

@inject
def run(
        consumer_file_uploaded: ConsumerFileUploaded = Provide[FileProcessingContainer.consumer_file_uploaded],
        tracking : TrackingService= Provide[apps_containers.tracking.TrackingContainer.tracking]
):
    logg= tracking.get_logger(__file__)
    print("start consumer")
    # while True:
    #     print("OK")
    #     logg.info("OK")
    #
    #     time.sleep(1)
    consumer_file_uploaded.start()


register_processing(run, depend_containers=[apps_containers.tracking.TrackingContainer])()
