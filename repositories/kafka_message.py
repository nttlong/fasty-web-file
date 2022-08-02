import os.path
import pathlib
import json
from kafka import KafkaProducer
from kafka.errors import KafkaError



# Asynchronous by default
from pip._internal import self_outdated_check

from must_implement import MustImplement
from .base_message import BaseMessage
@MustImplement()
class KafkaMessageRepository(BaseMessage):
    def __init__(self,tmp_data_dir:str,config:dict):
        self.tmp_dir = tmp_data_dir
        self.config = config.get('brokers')
        self.producer:KafkaProducer = KafkaProducer(bootstrap_servers=self.config)

    def send_dict_data(self,group_id:str,data:dict):
        future = self.producer.send(group_id, str.encode(json.dumps(data)))
    def append_binary_content_to_temp(self, app_name, relative_path, b_data):
        full_file_path = os.path.join(self.tmp_dir, app_name,relative_path).replace('/',os.sep)
        full_dir_path =str(pathlib.Path(full_file_path).parent)
        if not os.path.isdir(full_dir_path):
            os.makedirs(full_dir_path)
        mode ='bw'
        if os.path.isfile(full_file_path):
            mode='ba'
        with open(full_file_path,mode) as f:
            f.write(b_data)

    def get_content_location(self, app_name, relative_path):
        full_file_path = os.path.join(self.tmp_dir, app_name, relative_path).replace('/', os.sep)
        return full_file_path
