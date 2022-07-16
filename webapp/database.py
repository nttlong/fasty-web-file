from ReCompact.db_async import get_db_context,DbContext,get_connection
from contextlib import contextmanager, AbstractContextManager
from typing import Callable
import logging
from .contex import AppContext
logger = logging.getLogger(__name__)



class DbConnection:
    def __init__(self,  db_config:dict,app_context :AppContext):
        self.config=db_config
        self.app_context = app_context
        self.connection= get_connection(db_config)
        self.db_name= db_config.get('authSource')


    # @contextmanager
    def session(self) -> DbContext:

        return get_db_context(self.app_context.get_db_name())