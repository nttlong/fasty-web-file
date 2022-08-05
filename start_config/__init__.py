import os.path
import pathlib
import sys

import threading

__root_config__dir__ = None
__lock__ = threading.Lock()

__working_dir__ = str(pathlib.Path(__file__).parent.parent)


def get_config_path() -> str:
    global __root_config__dir__
    global __lock__
    if __root_config__dir__ is None:
        __lock__.acquire()
        try:
            dev_run_mdl = sys.modules.get("developer")
            if dev_run_mdl and hasattr(dev_run_mdl, "developer_mode"):
                import yaml
                boostrap_yaml_path = os.path.join(__working_dir__, "developer", "boostrap.yml")
                with open(boostrap_yaml_path, 'rb') as f:
                    data = yaml.safe_load(f)
                    __root_config__dir__ = data.get('config-path')
                    __root_config__dir__=os.path.join("developer",__root_config__dir__)
            else:
                __root_config__dir__="config.yml"

        finally:
            __lock__.release()

    return __root_config__dir__
