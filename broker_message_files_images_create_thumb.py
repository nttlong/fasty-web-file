import mimetypes
import time

from kafka import KafkaConsumer,KafkaProducer
from broker_group_const import MSG_GROUP_FILE_IMAGE_CREATE_THUMBS
import broker_group_const

import brokers_services.configs
import json
from PIL import Image
def run():
    consumer:KafkaConsumer= brokers_services.configs.create_consumer(
        MSG_GROUP_FILE_IMAGE_CREATE_THUMBS
    )
    producer = KafkaProducer(bootstrap_servers=brokers_services.configs.get_config().get('brokers'))

    while True:
        time.sleep(1)
        for message in consumer:
            data = json.loads(json.loads(message.value.decode("utf-8")))
            content_location = data.get('content_location')
            app_name = data.get('app_name')
            if app_name is None:
                continue


            # creating a object
            image = Image.open(content_location)
            MAX_SIZE = (100, 100)

            image.thumbnail(MAX_SIZE)

            # creating thumbnail
            image.save('pythonthumb.png')
            image.show()








run()