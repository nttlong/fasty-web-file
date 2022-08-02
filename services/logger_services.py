import logging
import os.path
import pathlib


class LoggerService:
    def __init__(self,working_dir):
        self.working_dir = working_dir
        self.log_directory = os.path.join(self.working_dir, "logs")
        if not os.path.isdir(self.working_dir):
            os.makedirs(self.working_dir)
        fileh = logging.FileHandler(self.log_directory, 'a')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileh.setFormatter(formatter)

        self.log = logging.getLogger()  # root logger
        for hdlr in self.log.handlers[:]:  # remove all old handlers
            self.log.removeHandler(hdlr)
        self.log.addHandler(fileh)  # set

    def error(self, ex):
        self.log.debug(ex)
