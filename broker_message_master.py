import mimetypes
import time

from kafka import KafkaConsumer,KafkaProducer
from broker_group_const import MSG_GROUP_FILE_UPLOADED
import broker_group_const

import brokers_services.configs
import json
def run():
    consumer:KafkaConsumer= brokers_services.configs.create_consumer(
        MSG_GROUP_FILE_UPLOADED
    )
    producer = KafkaProducer(bootstrap_servers=brokers_services.configs.get_config().get('brokers'))

    while True:
        time.sleep(1)
        for message in consumer:
            data = json.loads(json.loads(message.value.decode("utf-8")))
            content_path = data.get('content_location')
            app_name = data.get('app_name')
            if app_name is None:
                continue
            mime_type,_ = mimetypes.guess_type(content_path)
            if 'image/' in mime_type:
                post_data = dict(

                    content_location=content_path,
                    app_name = app_name
                )
                b_post_data = brokers_services.configs.dict_to_binary(post_data)
                future = producer.send(
                    broker_group_const.MSG_GROUP_FILE_IMAGE_CREATE_THUMBS,
                    b_post_data
                )


            print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key,
                                                 message.value))



run()