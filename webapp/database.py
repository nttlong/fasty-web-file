import ReCompact.db_async
from ReCompact.db_async import get_db_context,DbContext,get_connection
import logging

logger = logging.getLogger(__name__)


class DbConnection:
    def __init__(self,  db_config:dict,app_context):
        self.config=db_config
        self.app_context = app_context
        self.connection= get_connection(db_config)
        self.db_name= db_config.get('authSource')
        if int(ReCompact.db_async.db_version_info[0])>4:
            raise Exception(f"The system does not support with mongodb {ReCompact.db_async.db_version}\n"
                            f"It only support with mongodb verion 4")


    def session(self,db_name:str) -> DbContext:

        return get_db_context(db_name)