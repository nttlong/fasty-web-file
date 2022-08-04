import os.path

from PIL import Image


class BaseFileProcessFileService:
    def __init__(self, config: dict):
        self.config = config
        self.temp_dir = config.get('content-processing').get('temp-dir')
        if not os.path.isdir(self.temp_dir):
            raise Exception(f"{self.temp_dir} was not found, preview config.yml")


