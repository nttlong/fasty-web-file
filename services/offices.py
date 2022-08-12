import os
import pathlib
import subprocess
import typing
import uuid

import cv2

import app_logs
from services.base_files import BaseFileProcessFileService


class OfficeFileService(BaseFileProcessFileService):
    def __init__(self, config: dict):
        BaseFileProcessFileService.__init__(self, config)
        self.temp_dir_thumb = os.path.join(self.temp_dir, "office-thumb")
        if not os.path.isdir(self.temp_dir_thumb):
            os.makedirs(self.temp_dir_thumb)
        self.libre_office_path = config.get("libre-office-path")
        if self.libre_office_path is None:
            app_logs.debug(f"'libre-office-path' was not found in config.yml")
            print(f"'libre-office-path' was not found in config.yml")
            raise Exception(f"'libre-office-path' was not found in config.yml")
        if not os.path.isfile(self.libre_office_path):
            app_logs.debug(f"'{self.libre_office_path}' was not found")
            print(f"'{self.libre_office_path}' was not found")
            raise Exception(f"'{self.libre_office_path}' was not found")

    def create_image_from_office_file(self, relative_office_file_path, full_office_file_path):
        if not os.path.isfile(full_office_file_path):
            raise Exception(f"{full_office_file_path} was not found")
        out_put_dir = str(pathlib.Path(os.path.join(self.temp_dir_thumb, relative_office_file_path)).parent)
        if not os.path.isdir(out_put_dir):
            os.makedirs(out_put_dir)
        user_profile_id = str(uuid.uuid4())
        full_user_profile_path = os.path.join(self.temp_dir_thumb, "user-profiles", user_profile_id)
        if not os.path.isdir(user_profile_id):
            os.makedirs(full_user_profile_path)
        uno = f"Negotiate=0,ForceSynchronous=1;"
        # arg = f"--outdir {out_put_dir} {full_office_file_path.replace(os.sep, '/')}"
        # cmd_line ="libreoffice"
        # arg_list = [
        #     f'{self.libre_office_path}',
        #
        #     "--headless",
        #     "--convert-to png",
        #     # f"--accept={uno}",
        #     # f"-env:UserInstallation=file://{full_user_profile_path.replace(os.sep, '/')}",
        #     arg
        # ]
        # arg_list =[
        #
        #     "--headless",
        #     "--convert-to png",
        #     # f"--accept={uno}",
        #     # f"-env:UserInstallation=file://{full_user_profile_path.replace(os.sep, '/')}",
        #     arg
        # ]
        # full_comand_line = " ".join(arg_list)
        # # pid = subprocess.Popen([
        # #     self.libre_office_path,
        # #     full_comand_line
        # # ])
        # print(full_comand_line)
        # app_logs.info(full_comand_line)
        # print(f"Create image from office file {relative_office_file_path}")
        # app_logs.info(f"Create image from office file {relative_office_file_path} ")
        """
        p = Popen([LIBRE_OFFICE, '--headless', '--convert-to', 'pdf', '--outdir',
               out_folder, input_docx])
            `print([LIBRE_OFFICE, '--convert-to', 'pdf', input_docx])
            p.communicate()`
        """
        pid = subprocess.Popen(
            [
                self.libre_office_path,
                '--headless',
                '--convert-to', 'png',
                f"--accept={uno}",
                f"-env:UserInstallation=file://{full_user_profile_path.replace(os.sep, '/')}",
                '--outdir',
                out_put_dir, full_office_file_path
            ],
            shell=False
        )
        # pid = subprocess.run(
        #     full_comand_line
        # )

        ret = pid.communicate()  # Đợi
        return os.path.join(out_put_dir, f"{pathlib.Path(relative_office_file_path).stem}.png")
