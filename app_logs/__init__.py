import logging
import os.path
import pathlib
import sys
import traceback
print("app_logs start")
working_dir = str(pathlib.Path(__file__).parent.parent)
print(f"{__name__} wokring dir :{working_dir}")
if hasattr(sys.modules["__main__"],"__file__"):
    __main_file_path__ =pathlib.Path(sys.modules["__main__"].__file__).name.split('.')[0]
else:
    __main_file_path__="web_api"
print(f"Consumer name {__main_file_path__}")
log_directory = os.path.join(working_dir,"logs",__main_file_path__)
print(f"log file  path '{log_directory}'")
if not os.path.isdir(log_directory):
    os.makedirs(log_directory)
log_file_path = os.path.join(log_directory,"log.txt")

fileh = logging.FileHandler(log_file_path, 'a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileh.setFormatter(formatter)

logger = logging.Logger(__main_file_path__)

logger.addHandler(fileh)

logger.info("logger creating")
def debug(e):

    global logger
    global __dev_mode__
    if __dev_mode__:
        print(str(e))
    track = traceback.format_exc()
    logger.debug(track)
    logger.debug(e)

__dev_mode__=False
def set_developer_mode(mode:bool):
    __dev_mode__ =mode


def info(e):
    global logger
    global __dev_mode__
    if __dev_mode__:
        print(str(e))
    track = traceback.format_exc()
    logger.info(e)
logger.info("logger created")