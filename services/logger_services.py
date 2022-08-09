# import logging
# import os.path
# import pathlib
# import threading
#
# import app_logs
# import sys
# __main_file_name__ = pathlib.Path(sys.modules["__main__"].__file__).name.split('.')[0]
# __logger__ = None
# __lock__ = threading.Lock()
# class LoggerService:
#     def __init__(self,working_dir):
#         global __logger__
#         if __logger__ is None:
#             try:
#                 __lock__.acquire()
#                 global __main_file_name__
#                 self.working_dir = working_dir
#                 self.log_directory = os.path.join(self.working_dir,"logs",__main_file_name__)
#                 if not os.path.isdir(self.log_directory):
#                     os.makedirs(self.log_directory)
#                 self.log_file_path = os.path.join(self.log_directory,"service_logs.txt")
#                 fileh = logging.FileHandler(self.log_file_path, 'a')
#                 formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#                 fileh.setFormatter(formatter)
#                 __logger__ = logging.Logger(__name__)
#                 __logger__.addHandler(fileh)
#                 self.log = __logger__# root logger
#                 __logger__.info("Init log service is ok")
#                 print("Init log service is ok")
#             except Exception as ex:
#                 print("Can not init log")
#                 raise
#             finally:
#                 __lock__.release()
#         else:
#             self.log = __logger__
#
#
#     def error(self, ex):
#         self.log.debug(ex)
