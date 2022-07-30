import must_implement


@must_implement.MustDeclare()
class UploadedFile:
    message_type=(str)
    relative_file_path =(str)
    def __init__(self):
        self.message_type="message.file.upload"