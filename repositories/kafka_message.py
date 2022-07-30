from kafka import KafkaProducer
from kafka.errors import KafkaError



# Asynchronous by default
from pip._internal import self_outdated_check

from must_implement import MustImplement
from .base_message import BaseMessage
@MustImplement()
class KafkaMessageRepository(BaseMessage):
    def __init__(self,config:dict):
        self.config = config.get('brokers')
        self.producer:KafkaProducer = KafkaProducer(bootstrap_servers=self.config)

    def send_dict_data(self,group_id:str,data:dict):
        future = self.producer.send(group_id, b'raw_bytes')
