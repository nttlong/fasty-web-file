import logging
import pathlib
import os
import threading


working_dir = str(pathlib.Path(__file__).parent.parent)
log_directory = os.path.join(working_dir, "logs")
if not os.path.isdir(log_directory):
    os.makedirs(log_directory)

__cache__= {}
__lock__ = threading.Lock()
class TrackingService:
    def __init__(self):
        pass

    def get_logger(self, log_dir)->logging.Logger:
        if os.path.isfile(log_dir):
            log_dir = pathlib.Path(log_dir).name.split('.')[0]
        global __cache__
        global __lock__
        global log_directory
        full_log_dir=""
        if __cache__.get(log_dir) is None:
            __lock__.acquire()
            try:
                full_log_dir = os.path.join(log_directory, log_dir)
                if not os.path.isdir(full_log_dir):
                    os.makedirs(full_log_dir)
                print(f"log directory '{full_log_dir}'")
                log_file_path = os.path.join(full_log_dir, "log.txt")
                fileh = logging.FileHandler(log_file_path, 'a')
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                fileh.setFormatter(formatter)
                logger = logging.Logger(log_dir)  # root logger

                logger.addHandler(fileh)
                __cache__[log_dir] = logger
            except Exception as e:
                print(f"fail to connect log directory '{full_log_dir}'")
                print(e)
            finally:
                __lock__.release()
        return __cache__.get(log_dir)

