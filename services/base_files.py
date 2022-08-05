import os.path
import pathlib

from PIL import Image

__working_dir__=str(pathlib.Path(__file__).parent.parent)
class BaseFileProcessFileService:
    def __init__(self, config: dict):
        self.config = config
        self.temp_dir = config.get('content-processing').get('temp-dir')
        if self.temp_dir[0:2]=="./":
            self.temp_dir=self.temp_dir[2:]
            self.temp_dir= os.path.join(__working_dir__,self.temp_dir)
            if not os.path.isdir(self.temp_dir):
                os.makedirs(self.temp_dir)
        if not os.path.isdir(self.temp_dir):
            raise Exception(f"{self.temp_dir} was not found, preview config.yml")


