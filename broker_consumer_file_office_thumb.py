import sys

import app_logs
from repositories.kafka_consumers.message_file_thumb_office import ConsumerFileOfficeProcessThumb

if "dev" in sys.argv:
    import developer
import apps_containers.utils
from apps_containers.media_content import MediaContainer
from brokers_services import register_processing
from dependency_injector.wiring import Provide, inject
from brokers_services.containers import FileProcessingContainer
from repositories.kafka_consumers.message_file_thumb_video import ConsumerFileVideoProcessThumb
from start_config import get_config_path
app_logs.info("start")
print("start")
@inject
def run(
        consumer_file_video_process_thumb: ConsumerFileOfficeProcessThumb = Provide[
            FileProcessingContainer.consumer_file_office_process_thumb]):
    consumer_file_video_process_thumb.start()


register_processing(run, depend_containers=[
    MediaContainer,
    apps_containers.utils.UtilsContainer
])()
