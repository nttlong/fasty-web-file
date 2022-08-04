import apps_containers.utils
from apps_containers.media_content import MediaContainer
from brokers_services import register_processing
from dependency_injector.wiring import Provide, inject
from brokers_services.containers import FileProcessingContainer
from repositories.kafka_consumers.message_file_thumb import ConsumerFileImageProcessThumb


@inject
def run(
        consumer_file_image_process_thumb: ConsumerFileImageProcessThumb = Provide[
            FileProcessingContainer.consumer_file_image_process_thumb]):
    consumer_file_image_process_thumb.start()


register_processing(run, depend_containers=[
    MediaContainer,
    apps_containers.utils.UtilsContainer
])()
