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

    def __init__(self):
        self.message_type = "message.file.upload"
