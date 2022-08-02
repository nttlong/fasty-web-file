import os.path
import pathlib
import threading
import uuid
import json
import yaml
from kafka import KafkaConsumer
__config__:dict = None
__lock__= threading.Lock()
def get_config()->dict:
    global __config__
    global __lock__
    if __config__  is None:
        __lock__.acquire()
        try:
            current_path = os.path.join(str(pathlib.Path(__file__).parent), "config.yml")
            with open(current_path) as stream:
                __config__ =yaml.safe_load(stream)
        finally:
            __lock__.release()

    return __config__

get_config()

output_dir = __config__.get('out-put-dir')
if not os.path.isdir(output_dir):
    raise Exception(f"{output_dir} was not found")
group_id= f"group_{uuid.uuid4()}"

def dict_to_binary(data:dict)->bytes:
    ret=str.encode(json.dumps(data))
    return ret


def create_consumer(topic_id)->KafkaConsumer:
    global group_id
    ret = KafkaConsumer(
        topic_id,
        group_id=group_id,
        bootstrap_servers=get_config().get('brokers'),
        value_deserializer=lambda v: json.dumps(v.decode("utf-8")).encode("utf-8"),
        auto_offset_reset='earliest'
    )
    return ret
