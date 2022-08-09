from kafka.errors import KafkaTimeoutError

import repositories.base_message
import services.message_data_types as msg_dataTypes
from must_implement import get_dict
import threading
import app_logs
class MessageServices:
    def __init__(self,msg_repo:repositories.base_message.BaseMessage):
        app_logs.debug(f"init service {type(self)}")
        self.message_repository:repositories.base_message.BaseMessage = msg_repo
    def send_message_upload_file_to_brokers(self,msg:msg_dataTypes.UploadedFile):
        def run():
            try:
                return self.message_repository.send_dict_data(
                    group_id=msg.message_type,
                    data=get_dict(msg)
                )
            except KafkaTimeoutError as ex_timeout:
                print("Send message to kafka is timeout")
                app_logs.debug(ex_timeout)
            except Exception as ex:
                print("Send message to kafka error")
                app_logs.debug(ex)
        try:
            th= threading.Thread(target=run,args=())
            th.start()
        except Exception as e:
            app_logs.debug(e)

    def append_binary_content_to_temp(self, app_name:str, relative_path:str, b_data:bytes):
        self.message_repository.append_binary_content_to_temp(app_name,relative_path,b_data)

    def get_content_location(self, app_name, relative_path):
        return self.message_repository.get_content_location(app_name,relative_path)

