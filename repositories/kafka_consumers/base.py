import os.path
import pathlib
import sys
import time
import uuid
from typing import TypeVar

import syncer

# from services.logger_services import LoggerService
import app_logs

T = TypeVar("_T")
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
import json
from must_implement import new_instance

__working_dir__ = str(pathlib.Path(__file__).parent.parent.parent)
class FileProcessMessage:
    app_name = (str, True)
    """
    app_name 
    """
    relative_file_path = (str, True)
    upload_id = (str, True)
    message_type = (str, True)
    content_location = (str, True)
    """
    Full path to content where file has been uploaded
    """


class BaseConsumer:
    def __init__(self, config: dict, topic_id: str):
        def run_init():
            global __working_dir__
            # self.logger: LoggerService = logger
            self.config = config
            self.share_storage = config.get('message').get('share-storage')
            if self.share_storage is None:
                raise Exception('share-storage was not found at message in config.yml')
            if self.share_storage[0:2] == "./":
                self.share_storage = self.share_storage[2:]
                self.share_storage = os.path.join(__working_dir__, self.share_storage)
                if not os.path.isdir(self.share_storage):
                    os.makedirs(self.share_storage)
            self.storage_dir = self.config.get('message').get('temp-dir')
            if self.storage_dir[0:2] == './':
                self.storage_dir = self.storage_dir[2:]
                self.storage_dir = os.path.join(__working_dir__, self.storage_dir)
                if not os.path.isdir(self.storage_dir):
                    os.makedirs(self.storage_dir)
            if not os.path.isdir(self.storage_dir):
                raise Exception(f"{self.storage_dir} was not found. Preview config.yml at 'message/temp-dir'")
            self.brokers = self.config.get('message').get(self.config.get('message').get('type')).get('brokers')
            self.topic_id = topic_id
            self.group_id = f"g_{uuid.uuid4()}"
            print("-init consumer")
            print(f"- brokers-server:{','.join(self.brokers)}")
            print(f"- topic :{self.topic_id}")
            print(f"- group :{self.group_id}")
            self.__consumer__ = None
            app_logs.info("Start comsumer repository is ok")
        # try:
        #     run_init()
        #
        # except Exception as ex:
        #     app_logs.debug(ex)
        run_init()

    @property
    def consumer(self) -> KafkaConsumer:
        if self.__consumer__ == None:
            try:
                self.__consumer__: KafkaConsumer = KafkaConsumer(
                    self.topic_id,
                    group_id=self.group_id,
                    bootstrap_servers=self.brokers,
                    value_deserializer=lambda v: json.dumps(v.decode("utf-8")).encode("utf-8"),
                    auto_offset_reset='earliest'
                )
            except Exception as ex:
                app_logs.debug(ex)
                print("-init consumer fail")
        return self.__consumer__

    def get_msg_data(self, msg: ConsumerRecord):
        return json.loads(json.loads(msg.value.decode('utf-8')))

    def convert_msg_to(self, msg: ConsumerRecord, cls_type: T) -> T:
        data = self.get_msg_data(msg)
        ret: T = new_instance(cls_type, data)
        return ret

    def convert_dict_to_binary(self, data: dict):
        return str.encode(json.dumps(data))

    def convert_object_to_binary(self, obj) -> bytes:
        if obj is None:
            return b""
        if obj.__dict__.get("__field_data__"):
            return self.convert_dict_to_binary(obj.__dict__.get("__field_data__", {}))
        keys = [x for x in obj.__dict__.keys() if x[0:2] != "__" or x[-2:] != "__"]

        data = {}
        for k in keys:
            data[k] = obj.__dict__.get(k, None)
        return self.convert_dict_to_binary(data)

    def start(self):
        print("start")
        app_logs.info("start")
        time.sleep(0.3)
        while True:
            time.sleep(0.3)
            if "dev" in sys.argv:
                syncer.sync(self.run())
            else:
                try:
                    syncer.sync(self.run())
                except Exception as e:
                    print("error")
                    print(str(e))
                    app_logs.debug(e)

    def start1(self):
        print("start")
        time.sleep(0.3)
        while True:
            time.sleep(0.3)
            print("OK")

    def start_in_thread(self):
        print("start_in_thread")
        try:
            import threading
            th = threading.Thread(target=self.start1, args=(self))
            print("start thread")

            th.start()
            th.join(0.5)
            print("join thread")
        except Exception as e:
            app_logs.debug(e)
    def get_full_path_from_share_storage(self,app_name, relative_file_path):
        return os.path.join(self.share_storage,app_name, relative_file_path)