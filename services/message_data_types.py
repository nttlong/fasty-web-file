import broker_group_const
import must_implement


@must_implement.MustDeclare()
class UploadedFile:
    message_type = str
    """
    Message type when send to broker server
    """
    relative_file_path = (str, True)
    content_location = (str,True)
    """
    The accessible content in local file system
    """
    app_name=(str,True)
    """
    The name of application has sent this message
    """
    upload_id =(str,True)
    def __init__(self):
        self.message_type = broker_group_const.MSG_GROUP_FILE_UPLOADED
