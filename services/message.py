import repositories.base_message
import services.message_data_types as msg_dataTypes

class MessageServices:
    def __init__(self,msg_repo:repositories.base_message.BaseMessage):
        self.message_repository:repositories.base_message.BaseMessage = msg_repo

    def send_message_upload_file_to_brokers(self,msg:msg_dataTypes.UploadedFile):
        from must_implement import get_dict
        return self.message_repository.send_dict_data(
            group_id=msg.message_type,
            data= get_dict(msg)
        )

    def append_binary_content_to_temp(self, app_name:str, relative_path:str, b_data:bytes):
        self.message_repository.append_binary_content_to_temp(app_name,relative_path,b_data)

    def get_content_location(self, app_name, relative_path):
        return self.message_repository.get_content_location(app_name,relative_path)

