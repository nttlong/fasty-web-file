from ReCompact.db_async import get_db_context,DbContext,get_connection
import logging

logger = logging.getLogger(__name__)


class DbConnection:
    def __init__(self,  db_config:dict,app_context):
        self.config=db_config
        self.app_context = app_context
        self.connection= get_connection(db_config)
        self.db_name= db_config.get('authSource')



    def session(self,db_name:str) -> DbContext:

        return get_db_context(db_name)