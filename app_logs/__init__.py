import logging
import os.path
import pathlib
working_dir = str(pathlib.Path(__file__).parent.parent)
log_directory = os.path.join(working_dir, "logs")
if not os.path.isdir(log_directory):
    os.makedirs(log_directory)
log_file_path = os.path.join(log_directory,"log.txt")

fileh = logging.FileHandler(log_file_path, 'a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileh.setFormatter(formatter)

logger = logging.getLogger()  # root logger
for hdlr in logger.handlers[:]:  # remove all old handlers
    logger.removeHandler(hdlr)
logger.addHandler(fileh)


def debug(e):
    global logger
    logger.debug(e)