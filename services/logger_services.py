import logging
import os.path
import pathlib
import app_logs

class LoggerService:
    def __init__(self,working_dir):
        self.working_dir = working_dir
        self.log_directory = os.path.join(self.working_dir, "logs")
        if not os.path.isdir(self.log_directory):
            os.makedirs(self.log_directory)
        self.log_file_path = os.path.join(self.log_directory,"service_logs.txt")
        fileh = logging.FileHandler(self.log_file_path, 'a')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileh.setFormatter(formatter)

        self.log = logging.Logger(__name__)  # root logger

        self.log.addHandler(fileh)  # set

    def error(self, ex):
        self.log.debug(ex)
