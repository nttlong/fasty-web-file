import os
import pathlib
import uuid

import cv2

import app_logs
from services.base_files import BaseFileProcessFileService


class VideoFileService(BaseFileProcessFileService):
    def __init__(self, config: dict):
        BaseFileProcessFileService.__init__(self, config)
        self.temp_dir_thumb = os.path.join(self.temp_dir, "video-thumb")
        if not os.path.isdir(self.temp_dir_thumb):
            os.makedirs(self.temp_dir_thumb)

    def extract_framTo_imag(self, full_path_to_file:str):
        """
        Extract  frame in middle video to image file
        """
        thumb_file_name= pathlib.Path(full_path_to_file).name.split('.')[0]
        # png_thumb=f"{thumb_file_name}.png"
        full_png_file_path = os.path.join(self.temp_dir_thumb, str(uuid.uuid4()), f"{thumb_file_name}.png")
        dir_of_image_path = str(pathlib.Path(full_png_file_path).parent)
        if not os.path.isdir(dir_of_image_path):
            os.makedirs(dir_of_image_path)

        vcap = cv2.VideoCapture(full_path_to_file)

        fps = vcap.get(cv2.CAP_PROP_FPS)  # OpenCV v2.x used "CV_CAP_PROP_FPS"
        frame_count = int(vcap.get(cv2.CAP_PROP_FRAME_COUNT))

        middel_frame,_ = divmod(frame_count,2)
        vcap.set(cv2.CAP_PROP_POS_MSEC, middel_frame)
        success, image = vcap.read()
        if not success:
            print(f"Extract frame  to {full_png_file_path} is fail")
            app_logs.debug(f"Extract frame  to {full_png_file_path} is fail")
        cv2.imwrite( full_png_file_path, image)
        print(f"Extract frame  to {full_png_file_path} is ok")
        app_logs.debug(f"Extract frame  to {full_png_file_path} is ok")
        return full_png_file_path