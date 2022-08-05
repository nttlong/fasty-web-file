import os.path
import ntpath
import pathlib
import uuid

from PIL import Image

from services.base_files import BaseFileProcessFileService


class ImageFileService(BaseFileProcessFileService):
    def __init__(self, config: dict):
        BaseFileProcessFileService.__init__(self, config)
        self.temp_dir_thumb = os.path.join(self.temp_dir, "thumb")
        if not os.path.isdir(self.temp_dir_thumb):
            os.makedirs(self.temp_dir_thumb)

    def create_thumb(self, path_to_file: str, thumb_width: int, thumb_height: int):
        # importing Image class from PIL package

        # creating a object
        image = Image.open(path_to_file)
        MAX_SIZE = (thumb_width, thumb_height)

        thumb_file_name = pathlib.Path(path_to_file).name.split('.')[0]

        full_thumb_file_path = os.path.join(self.temp_dir_thumb, str(uuid.uuid4()), f"{thumb_file_name}.webp")
        full_thumb_dir_path =str(pathlib.Path(full_thumb_file_path).parent)
        if not os.path.isdir(full_thumb_dir_path):
            os.makedirs(full_thumb_dir_path)
        image.thumbnail(MAX_SIZE)

        # creating thumbnail
        image.save(full_thumb_file_path,format="webp")
        return full_thumb_file_path
