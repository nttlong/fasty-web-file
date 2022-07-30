import repositories.base_message
import services.message_data_types as msg_dataTypes

class MessageServices:
    def __init__(self,msg_repo:repositories.base_message.BaseMessage):
        self.message_repository:repositories.base_message.BaseMessage = msg_repo

    def send_message_upload_file_to_brokers(self,msg:msg_dataTypes.UploadedFile):
        pass

